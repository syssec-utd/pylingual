from __future__ import absolute_import, division, print_function
__metaclass__ = type
import json
import pytest
from ansible.module_utils.basic import missing_required_lib
from .....plugins.module_utils._hashi_vault_common import HashiVaultValueError
from .....plugins.modules import vault_kv2_write
from ...compat import mock
hvac = pytest.importorskip('hvac')
pytestmark = pytest.mark.usefixtures('patch_ansible_module', 'patch_authenticator', 'patch_get_vault_client')

def _connection_options():
    return {'auth_method': 'token', 'url': 'http://myvault', 'token': 'beep-boop'}

def _sample_options():
    return {'engine_mount_point': 'secret', 'path': 'endpoint', 'data': {'foo': 'bar'}}

def _combined_options(**kwargs):
    opt = _connection_options()
    opt.update(_sample_options())
    opt.update(kwargs)
    return opt

class TestModuleVaultKv2Write:

    @pytest.mark.parametrize('patch_ansible_module', [_combined_options()], indirect=True)
    @pytest.mark.parametrize('exc', [HashiVaultValueError('throwaway msg'), NotImplementedError('throwaway msg')])
    def test_vault_kv2_write_authentication_error(self, authenticator, exc, capfd):
        authenticator.authenticate.side_effect = exc
        with pytest.raises(SystemExit) as e:
            vault_kv2_write.main()
        (out, err) = capfd.readouterr()
        result = json.loads(out)
        assert e.value.code != 0, 'result: %r' % (result,)
        assert result['msg'] == 'throwaway msg', 'result: %r' % result

    @pytest.mark.parametrize('patch_ansible_module', [_combined_options()], indirect=True)
    @pytest.mark.parametrize('exc', [HashiVaultValueError('throwaway msg'), NotImplementedError('throwaway msg')])
    def test_vault_kv2_write_auth_validation_error(self, authenticator, exc, capfd):
        authenticator.validate.side_effect = exc
        with pytest.raises(SystemExit) as e:
            vault_kv2_write.main()
        (out, err) = capfd.readouterr()
        result = json.loads(out)
        assert e.value.code != 0, 'result: %r' % (result,)
        assert result['msg'] == 'throwaway msg'

    @pytest.mark.parametrize('patch_ansible_module', [_combined_options()], indirect=True)
    def test_vault_kv2_write_get_no_hvac(self, capfd):
        with mock.patch.multiple(vault_kv2_write, HAS_HVAC=False, HVAC_IMPORT_ERROR=None, create=True):
            with pytest.raises(SystemExit) as e:
                vault_kv2_write.main()
        (out, err) = capfd.readouterr()
        result = json.loads(out)
        assert e.value.code != 0, 'result: %r' % (result,)
        assert result['msg'] == missing_required_lib('hvac')

    @pytest.mark.parametrize('patch_ansible_module', [[_combined_options(read_before_write=True)]], indirect=True)
    @pytest.mark.parametrize('response', ({'thishasnodata': {}}, {'data': {'not data': {}}}))
    def test_vault_kv2_write_read_responses_invalid(self, vault_client, capfd, response):
        client = vault_client
        client.secrets.kv.v2.read_secret_version.return_value = response
        with pytest.raises(SystemExit) as e:
            vault_kv2_write.main()
        (out, err) = capfd.readouterr()
        result = json.loads(out)
        assert e.value.code != 0, 'result: %r' % (result,)
        assert 'Vault response did not contain data' in result['msg']

    @pytest.mark.parametrize('exc', [hvac.exceptions.VaultError('throwaway msg')])
    @pytest.mark.parametrize('patch_ansible_module', [_combined_options(read_before_write=True)], indirect=True)
    def test_vault_kv2_write_read_vault_error(self, vault_client, capfd, exc):
        client = vault_client
        client.secrets.kv.v2.read_secret_version.side_effect = exc
        with pytest.raises(SystemExit) as e:
            vault_kv2_write.main()
        (out, err) = capfd.readouterr()
        result = json.loads(out)
        assert e.value.code != 0, 'result: %r' % (result,)
        assert 'VaultError reading' in result['msg'], 'result: %r' % (result,)

    @pytest.mark.parametrize('exc', [hvac.exceptions.InvalidPath('throwaway msg')])
    @pytest.mark.parametrize('patch_ansible_module', [_combined_options()], indirect=True)
    def test_vault_kv2_write_write_invalid_path(self, vault_client, capfd, exc):
        client = vault_client
        client.secrets.kv.v2.create_or_update_secret.side_effect = exc
        with pytest.raises(SystemExit) as e:
            vault_kv2_write.main()
        (out, err) = capfd.readouterr()
        result = json.loads(out)
        assert e.value.code != 0, 'result: %r' % (result,)
        assert 'InvalidPath writing to' in result['msg'], 'result: %r' % (result,)