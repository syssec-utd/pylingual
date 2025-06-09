from __future__ import absolute_import, division, print_function
__metaclass__ = type
import json
from unittest.mock import MagicMock
import pytest
from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_text
from ansible.playbook.play_context import PlayContext
from ansible.plugins.loader import connection_loader
from ansible_collections.ansible.netcommon.plugins.connection.network_cli import terminal_loader

@pytest.fixture(name='conn')
def plugin_fixture(monkeypatch):
    pc = PlayContext()
    pc.network_os = 'fakeos'

    def get(*args, **kwargs):
        return MagicMock()
    monkeypatch.setattr(terminal_loader, 'get', get)
    conn = connection_loader.get('ansible.netcommon.network_cli', pc, '/dev/null')
    return conn

@pytest.mark.parametrize('network_os', [None, 'invalid'])
def test_network_cli_invalid_os(network_os):
    pc = PlayContext()
    pc.network_os = network_os
    with pytest.raises(AnsibleConnectionFailure):
        connection_loader.get('ansible.netcommon.network_cli', pc, '/dev/null')

@pytest.mark.parametrize('look_for_keys', [True, False, None])
@pytest.mark.parametrize('password', ['password', None])
@pytest.mark.parametrize('private_key_file', ['/path/to/key/file', None])
@pytest.mark.parametrize('ssh_type', ['paramiko', 'libssh', 'auto'])
def test_look_for_keys(conn, look_for_keys, password, private_key_file, ssh_type):
    conn.set_options(direct={'ssh_type': ssh_type, 'password': password, 'private_key_file': private_key_file})
    if look_for_keys is not None:
        conn.set_options(direct={'look_for_keys': look_for_keys})
        assert conn.ssh_type_conn.get_option('look_for_keys') is look_for_keys
    elif private_key_file:
        assert conn.ssh_type_conn.get_option('look_for_keys') is True
    elif password:
        assert conn.ssh_type_conn.get_option('look_for_keys') is False
    else:
        assert conn.ssh_type_conn.get_option('look_for_keys') is True

@pytest.mark.parametrize('ssh_type', ['paramiko', 'libssh', 'auto'])
def test_options_pass_through(conn, ssh_type):
    conn.set_options(direct={'ssh_type': ssh_type, 'host_key_checking': False, 'proxy_command': 'do a proxy'})
    assert conn.get_option('ssh_type') == ssh_type
    with pytest.raises(KeyError):
        conn.ssh_type_conn.get_option('ssh_type')
    assert conn.get_option('host_key_checking') is False
    assert conn.ssh_type_conn.get_option('host_key_checking') is False
    with pytest.raises(KeyError):
        conn.get_option('proxy_command')
    assert conn.ssh_type_conn.get_option('proxy_command') == 'do a proxy'

@pytest.mark.parametrize('has_libssh', (True, False))
def test_network_cli_ssh_type_auto(conn, has_libssh):
    """Test that ssh_type: auto resolves to the correct option."""
    from ansible_collections.ansible.netcommon.plugins.connection import network_cli
    network_cli.HAS_PYLIBSSH = has_libssh
    conn.set_options(direct={'ssh_type': 'auto'})
    if has_libssh:
        assert conn.ssh_type == 'libssh'
    else:
        assert conn.ssh_type == 'paramiko'

@pytest.mark.parametrize('become_method,become_pass', [('enable', 'password'), (None, None)])
def test_network_cli__connect(conn, become_method, become_pass):
    conn.ssh = MagicMock()
    conn.receive = MagicMock()
    conn._terminal = MagicMock()
    conn._ssh_type_conn = MagicMock()
    if become_method:
        conn._play_context.become = True
        conn._play_context.become_method = become_method
        conn._play_context.become_pass = become_pass
    conn._connect()
    assert conn._ssh_type_conn._connect.called is True
    assert conn._terminal.on_open_shell.called is True
    if become_method:
        conn._terminal.on_become.assert_called_with(passwd=become_pass)
    else:
        assert conn._terminal.on_become.called is False

@pytest.mark.parametrize('command', ['command', json.dumps({'command': 'command'})])
def test_network_cli_exec_command(conn, command):
    mock_send = MagicMock(return_value=b'command response')
    conn.send = mock_send
    conn._ssh_shell = MagicMock()
    conn._ssh_type_conn = MagicMock()
    out = conn.exec_command(command)
    mock_send.assert_called_with(command=b'command')
    assert out == b'command response'

@pytest.mark.parametrize('response', [b'device#command\ncommand response\n\ndevice#', pytest.param(b'ERROR: error message device#', marks=pytest.mark.xfail(raises=AnsibleConnectionFailure))])
@pytest.mark.parametrize('ssh_type', ['paramiko', 'libssh', 'auto'])
def test_network_cli_send(conn, response, ssh_type):
    conn.set_options(direct={'ssh_type': ssh_type, 'terminal_stderr_re': [{'pattern': '^ERROR'}], 'terminal_stdout_re': [{'pattern': 'device#'}]})
    mock__shell = MagicMock()
    conn._terminal = MagicMock()
    conn._ssh_shell = mock__shell
    conn._connected = True
    if conn.ssh_type == 'paramiko':
        mock__shell.recv.side_effect = [response, None]
    elif conn.ssh_type == 'libssh':
        mock__shell.read_bulk_response.side_effect = [response, None]
    conn.send(b'command')
    mock__shell.sendall.assert_called_with(b'command\r')
    assert to_text(conn._command_response) == 'command response'

def test_network_cli_close(conn):
    conn._terminal = MagicMock()
    conn._ssh_shell = MagicMock()
    conn._ssh_type_conn = MagicMock()
    conn._connected = True
    conn.close()
    assert conn._connected is False
    assert conn._terminal.on_close_shell.called is True
    assert conn._ssh_shell is None
    assert conn._ssh_type_conn is None