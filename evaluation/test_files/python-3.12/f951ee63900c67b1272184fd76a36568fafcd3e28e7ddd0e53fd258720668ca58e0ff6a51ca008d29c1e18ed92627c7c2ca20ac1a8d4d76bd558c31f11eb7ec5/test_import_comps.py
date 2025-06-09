from __future__ import absolute_import
import os
import sys
import unittest
import json
import pytest
import koji
import mock
import six
try:
    import libcomps
except ImportError:
    libcomps = None
try:
    import yum.comps as yumcomps
except ImportError:
    yumcomps = None
import koji_cli.commands
from koji_cli.commands import handle_import_comps, _import_comps, _import_comps_alt
from . import utils

class TestImportComps(utils.CliTestCase):

    def setUp(self):
        self.maxDiff = None
        self.options = mock.MagicMock()
        self.options.debug = False
        self.session = mock.MagicMock()
        self.session.getAPIVersion.return_value = koji.API_VERSION
        self.mock_activate_session = mock.patch('koji_cli.commands.activate_session').start()
        self.error_format = 'Usage: %s import-comps [options] <file> <tag>\n(Specify the --help global option for a list of other help options)\n\n%s: error: {message}\n' % (self.progname, self.progname)

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    @mock.patch('koji_cli.commands.libcomps')
    @mock.patch('koji_cli.commands._import_comps')
    @mock.patch('koji_cli.commands._import_comps_alt')
    def test_handle_import_comps_libcomps(self, mock_import_comps_alt, mock_import_comps, libcomps, stdout):
        filename = './data/comps-example.xml'
        tag = 'tag'
        tag_info = {'name': tag, 'id': 1}
        force = None
        args = [filename, tag]
        kwargs = {'force': force}
        self.session.getTag.return_value = tag_info
        rv = handle_import_comps(self.options, self.session, args)
        actual = stdout.getvalue()
        expected = ''
        self.assertMultiLineEqual(actual, expected)
        self.mock_activate_session.assert_called_once_with(self.session, self.options)
        self.session.getTag.assert_called_once_with(tag)
        mock_import_comps.assert_called_once_with(self.session, filename, tag, kwargs)
        mock_import_comps_alt.assert_not_called()
        self.assertNotEqual(rv, 1)

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    @mock.patch('koji_cli.commands.libcomps', new=None)
    @mock.patch('koji_cli.commands.yumcomps', create=True)
    @mock.patch('koji_cli.commands._import_comps')
    @mock.patch('koji_cli.commands._import_comps_alt')
    def test_handle_import_comps_yumcomps(self, mock_import_comps_alt, mock_import_comps, yumcomps, stdout):
        filename = './data/comps-example.xml'
        tag = 'tag'
        tag_info = {'name': tag, 'id': 1}
        force = True
        args = ['--force', filename, tag]
        local_options = {'force': force}
        self.session.getTag.return_value = tag_info
        rv = handle_import_comps(self.options, self.session, args)
        actual = stdout.getvalue()
        expected = ''
        self.assertMultiLineEqual(actual, expected)
        self.mock_activate_session.assert_called_once_with(self.session, self.options)
        self.session.getTag.assert_called_once_with(tag)
        mock_import_comps.assert_not_called()
        mock_import_comps_alt.assert_called_once_with(self.session, filename, tag, local_options)
        self.assertNotEqual(rv, 1)

    @mock.patch('koji_cli.commands.libcomps', new=None)
    @mock.patch('koji_cli.commands.yumcomps', new=None, create=True)
    @mock.patch('koji_cli.commands._import_comps')
    @mock.patch('koji_cli.commands._import_comps_alt')
    def test_handle_import_comps_comps_na(self, mock_import_comps_alt, mock_import_comps):
        filename = './data/comps-example.xml'
        tag = 'tag'
        tag_info = {'name': tag, 'id': 1}
        args = ['--force', filename, tag]
        self.session.getTag.return_value = tag_info
        self.assert_system_exit(handle_import_comps, self.options, self.session, args, stderr='comps module not available\n', exit_code=1, activate_session=None)
        self.mock_activate_session.assert_called_once_with(self.session, self.options)
        self.session.getTag.assert_called_once_with(tag)
        mock_import_comps.assert_not_called()
        mock_import_comps_alt.assert_not_called()

    @mock.patch('koji_cli.commands._import_comps')
    @mock.patch('koji_cli.commands._import_comps_alt')
    def test_handle_import_comps_tag_not_exists(self, mock_import_comps_alt, mock_import_comps):
        filename = './data/comps-example.xml'
        tag = 'tag'
        tag_info = None
        args = [filename, tag]
        self.session.getTag.return_value = tag_info
        self.assert_system_exit(handle_import_comps, self.options, self.session, args, stderr='No such tag: %s\n' % tag, exit_code=1, activate_session=None)
        self.mock_activate_session.assert_called_once_with(self.session, self.options)
        self.session.getTag.assert_called_once_with(tag)
        mock_import_comps.assert_not_called()
        mock_import_comps_alt.assert_not_called()

    def test_handle_import_comps_empty_args(self):
        args = []
        self.assert_system_exit(handle_import_comps, self.options, self.session, args, stdout='', stderr=self.format_error_message('Incorrect number of arguments'), exit_code=2, activate_session=None)
        self.mock_activate_session.assert_not_called()
        self.session.getTag.assert_not_called()
        self.session.getTagGroups.assert_not_called()
        self.session.groupListAdd.assert_not_called()

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    def _test_import_comps_libcomps(self, stdout):
        if libcomps is None:
            pytest.skip('no libcomps')
        comps_file = os.path.dirname(__file__) + '/data/comps-example.xml'
        stdout_file = os.path.dirname(__file__) + '/data/comps-example.libcomps.out'
        calls_file = os.path.dirname(__file__) + '/data/comps-example.libcomps.calls'
        self._test_import_comps(_import_comps, comps_file, stdout_file, calls_file, stdout)

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    def _test_import_comps_sample_libcomps(self, stdout):
        if libcomps is None:
            pytest.skip('no libcomps')
        comps_file = os.path.dirname(__file__) + '/data/comps-sample.xml'
        stdout_file = os.path.dirname(__file__) + '/data/comps-sample.libcomps.out'
        calls_file = os.path.dirname(__file__) + '/data/comps-sample.libcomps.calls'
        self._test_import_comps(_import_comps, comps_file, stdout_file, calls_file, stdout)

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    @mock.patch('koji_cli.commands.libcomps', new=None)
    @mock.patch('koji_cli.commands.yumcomps', create=True, new=yumcomps)
    def _test_import_comps_yumcomps(self, stdout):
        if yumcomps is None:
            pytest.skip('no yum.comps')
        comps_file = os.path.dirname(__file__) + '/data/comps-example.xml'
        stdout_file = os.path.dirname(__file__) + '/data/comps-example.yumcomps.out'
        calls_file = os.path.dirname(__file__) + '/data/comps-example.yumcomps.calls'
        self._test_import_comps(_import_comps_alt, comps_file, stdout_file, calls_file, stdout)

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    @mock.patch('koji_cli.commands.libcomps', new=None)
    @mock.patch('koji_cli.commands.yumcomps', create=True, new=yumcomps)
    def _test_import_comps_sample_yumcomps(self, stdout):
        if yumcomps is None:
            pytest.skip('no yum.comps')
        comps_file = os.path.dirname(__file__) + '/data/comps-sample.xml'
        stdout_file = os.path.dirname(__file__) + '/data/comps-sample.yumcomps.out'
        calls_file = os.path.dirname(__file__) + '/data/comps-sample.yumcomps.calls'
        self._test_import_comps(_import_comps_alt, comps_file, stdout_file, calls_file, stdout)

    def _test_import_comps(self, method, comps_file, stdout_file, calls_file, stdout):
        tag = 'tag'
        self.options.force = None
        rv = method.__call__(self.session, comps_file, tag, self.options)
        expected = ''
        with open(stdout_file, 'rb') as f:
            expected = f.read().decode('ascii')
        self.assertMultiLineEqual(stdout.getvalue(), expected)
        expected = []
        for c in json.load(open(calls_file, 'rt')):
            expected.append(getattr(mock.call, c[0]).__call__(*c[1], **c[2]))
        if hasattr(self.session, 'assertHasCalls'):
            self.session.assertHasCalls(expected)
        else:
            self.session.assert_has_calls(expected)
        self.assertNotEqual(rv, 1)

def _generate_out_calls(method, comps_file, stdout_file, calls_file):
    tag = 'tag'
    force = None
    options = {'force': force}
    session = mock.MagicMock()
    with open(stdout_file, 'wb') as f:
        orig_stdout = sys.stdout
        sys.stdout = f
        method.__call__(session, comps_file, tag, options)
        sys.stdout = orig_stdout
    with open(calls_file, 'wb') as f:
        f.write(str(session.mock_calls).encode('ascii') + '\n')

def generate_out_calls():
    """Generate .out and .calls files for tests.
    These files should be carefully check to make sure they're excepted"""
    path = os.path.dirname(__file__)
    comps_file = path + '/data/comps-example.xml'
    stdout_file = path + '/data/comps-example.libcomps.out'
    calls_file = path + '/data/comps-example.libcomps.calls'
    _generate_out_calls(_import_comps, comps_file, stdout_file, calls_file)
    comps_file = path + '/data/comps-sample.xml'
    stdout_file = path + '/data/comps-sample.libcomps.out'
    calls_file = path + '/data/comps-sample.libcomps.calls'
    _generate_out_calls(_import_comps, comps_file, stdout_file, calls_file)
    koji_cli.commands.yumcomps = yumcomps
    comps_file = path + '/data/comps-example.xml'
    stdout_file = path + '/data/comps-example.yumcomps.out'
    calls_file = path + '/data/comps-example.yumcomps.calls'
    _generate_out_calls(_import_comps_alt, comps_file, stdout_file, calls_file)
    comps_file = path + '/data/comps-sample.xml'
    stdout_file = path + '/data/comps-sample.yumcomps.out'
    calls_file = path + '/data/comps-sample.yumcomps.calls'
    _generate_out_calls(_import_comps_alt, comps_file, stdout_file, calls_file)
if __name__ == '__main__':
    unittest.main()