from __future__ import absolute_import, division, print_function
__metaclass__ = type
import pytest
from units.modules.utils import set_module_args, exit_json, fail_json, AnsibleExitJson
from ansible.module_utils import basic
from ansible_collections.check_point.mgmt.plugins.modules import cp_mgmt_verify_software_package
PAYLOAD = {'name': 'Check_Point_R80_40_JHF_MCD_DEMO_019_MAIN_Bundle_T1_VISIBLE_FULL.tgz', 'wait_for_task': False}
RETURN_PAYLOAD = {'task-id': '53de74b7-8f19-4cbe-99fc-a81ef0759bad'}
command = 'verify-software-package'
failure_msg = '{command failed}'

class TestCheckpointVerifySoftwarePackage(object):
    module = cp_mgmt_verify_software_package

    @pytest.fixture(autouse=True)
    def module_mock(self, mocker):
        return mocker.patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)

    @pytest.fixture
    def connection_mock(self, mocker):
        connection_class_mock = mocker.patch('ansible.module_utils.network.checkpoint.checkpoint.Connection')
        return connection_class_mock.return_value

    def test_command(self, mocker, connection_mock):
        connection_mock.send_request.return_value = (200, RETURN_PAYLOAD)
        result = self._run_module(PAYLOAD)
        assert result['changed']
        assert RETURN_PAYLOAD == result[command]

    def test_command_fail(self, mocker, connection_mock):
        connection_mock.send_request.return_value = (404, failure_msg)
        try:
            result = self._run_module(PAYLOAD)
        except Exception as e:
            result = e.args[0]
        assert 'Checkpoint device returned error 404 with message ' + failure_msg == result['msg']

    def _run_module(self, module_args):
        set_module_args(module_args)
        with pytest.raises(AnsibleExitJson) as ex:
            self.module.main()
        return ex.value.args[0]