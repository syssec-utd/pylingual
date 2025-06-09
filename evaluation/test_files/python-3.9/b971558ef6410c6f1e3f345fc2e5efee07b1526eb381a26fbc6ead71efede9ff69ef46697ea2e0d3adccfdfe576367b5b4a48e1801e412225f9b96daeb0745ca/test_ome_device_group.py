from __future__ import absolute_import, division, print_function
__metaclass__ = type
import pytest
import json
from ssl import SSLError
from io import StringIO
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_group
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils._text import to_text
netaddr = pytest.importorskip('netaddr')
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_device_group.'
ADD_STATIC_GROUP_MESSAGE = 'Devices can be added only to the static device groups created using OpenManage Enterprise.'
REMOVE_STATIC_GROUP_MESSAGE = 'Devices can be removed only from the static device groups created using OpenManage Enterprise.'
INVALID_IP_FORMAT = 'The format {0} of the IP address provided is not supported or invalid.'
IP_NOT_EXISTS = 'The IP addresses provided do not exist in OpenManage Enterprise.'
try:
    from netaddr import IPAddress, IPNetwork, IPRange
    HAS_NETADDR = True
except ImportError:
    HAS_NETADDR = False

@pytest.fixture
def ome_connection_mock_for_device_group(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    ome_connection_mock_obj.get_all_report_details.return_value = {'report_list': []}
    return ome_connection_mock_obj

class TestOMEDeviceGroup(FakeAnsibleModule):
    module = ome_device_group

    def test_ome_device_group_get_group_id_case01(self, ome_connection_mock_for_device_group, ome_response_mock):
        f_module = self.get_module_mock(params={'name': 'Storage Services', 'device_ids': [25011], 'device_service_tags': []})
        ome_response_mock.json_data = {'value': []}
        with pytest.raises(Exception) as exc:
            self.module.get_group_id(ome_connection_mock_for_device_group, f_module)
        assert exc.value.args[0] == "Unable to complete the operation because the entered target group name 'Storage Services' is invalid."
        ome_response_mock.json_data = {'value': [{'Id': 25011, 'CreatedBy': 'user', 'TypeId': 3000, 'MembershipTypeId': 12}]}
        resp = self.module.get_group_id(ome_connection_mock_for_device_group, f_module)
        assert resp == 25011

    def test_ome_device_group_get_group_id_case02(self, ome_connection_mock_for_device_group, ome_response_mock):
        f_module = self.get_module_mock(params={'group_id': 1234, 'device_ids': [25011], 'device_service_tags': []})
        ome_connection_mock_for_device_group.invoke_request.side_effect = HTTPError('http://testhost.com', 400, 'http error message', {'accept-type': 'application/json'}, StringIO(to_text(json.dumps({'info': 'error_details'}))))
        with pytest.raises(Exception) as exc1:
            self.module.get_group_id(ome_connection_mock_for_device_group, f_module)
        assert exc1.value.args[0] == "Unable to complete the operation because the entered target group Id '1234' is invalid."

    def test_ome_device_group_get_group_id_case03(self, ome_connection_mock_for_device_group, ome_response_mock):
        f_module = self.get_module_mock(params={'group_id': 1234, 'device_ids': [25011], 'device_service_tags': []})
        ome_response_mock.json_data = {'Id': 1234, 'CreatedBy': 'user', 'TypeId': 3000, 'MembershipTypeId': 12}
        resp = self.module.get_group_id(ome_connection_mock_for_device_group, f_module)
        assert resp == 1234

    def test_ome_device_group_get_device_id(self, ome_connection_mock_for_device_group):
        report_list = [{'Id': 25011, 'DeviceServiceTag': 'SEFRG2'}, {'Id': 25012, 'DeviceServiceTag': 'SEFRG3'}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {'report_list': report_list}
        f_module = self.get_module_mock(params={'name': 'Storage Services', 'device_ids': [25011, 25012]})
        (device_list, key) = self.module.get_device_id(ome_connection_mock_for_device_group, f_module)
        assert device_list == [25011, 25012]
        assert key == 'Id'
        f_module = self.get_module_mock(params={'name': 'Storage Services', 'device_service_tags': ['SEFRG2', 'SEFRG3']})
        (device_list, key) = self.module.get_device_id(ome_connection_mock_for_device_group, f_module)
        assert device_list == [25011, 25012]
        assert key == 'DeviceServiceTag'
        f_module = self.get_module_mock(params={'name': 'Storage Services', 'device_ids': [25011, 25000]})
        with pytest.raises(Exception) as exc:
            self.module.get_device_id(ome_connection_mock_for_device_group, f_module)
        assert exc.value.args[0] == "Unable to complete the operation because the entered target device id(s) '25000' are invalid."

    def test_ome_device_group_add_member_to_group(self, ome_connection_mock_for_device_group, ome_response_mock):
        report_list = [{'Id': 25011, 'DeviceServiceTag': 'SEFRG2'}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {'report_list': report_list}
        f_module = self.get_module_mock(params={'name': 'Storage Services', 'device_ids': [25011]})
        ome_response_mock.status_code = 204
        ome_response_mock.success = True
        with pytest.raises(Exception) as exc:
            self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group, 1, [25011], 'Id')
        assert exc.value.args[0] == 'No changes found to be applied.'
        f_module.check_mode = True
        with pytest.raises(Exception) as exc:
            self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group, 1, [25011], 'Id')
        assert exc.value.args[0] == 'No changes found to be applied.'
        f_module.check_mode = False
        report_list = [{'Id': 25013, 'DeviceServiceTag': 'SEFRG4'}, {'Id': 25014, 'DeviceServiceTag': 'SEFRG5'}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {'report_list': report_list}
        (resp, []) = self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group, 1, [25011, 25012], 'Id')
        assert resp.status_code == 204
        f_module.check_mode = True
        with pytest.raises(Exception) as exc:
            self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group, 1, [25011, 25012], 'Id')
        assert exc.value.args[0] == 'Changes found to be applied.'

    def test_ome_device_group_main_exception(self, ome_connection_mock_for_device_group, mocker, ome_response_mock, ome_default_args):
        ome_default_args.update({'name': 'Storage Services', 'device_ids': [25011, 25012]})
        ome_response_mock.status_code = 204
        ome_response_mock.success = True
        mocker.patch(MODULE_PATH + 'get_group_id', return_value=1)
        mocker.patch(MODULE_PATH + 'get_device_id', return_value=[25011, 25012])
        mocker.patch(MODULE_PATH + 'add_member_to_group', return_value=(ome_response_mock, []))
        result = self._run_module(ome_default_args)
        assert result['msg'] == 'Successfully added member(s) to the device group.'

    def test_ome_device_group_argument_exception_case1(self, ome_default_args):
        ome_default_args.update({'name': 'Storage Services', 'device_ids': [25011, 25012], 'group_id': 1234})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == 'parameters are mutually exclusive: name|group_id'

    def test_ome_device_group_argument_exception_case2(self, ome_default_args):
        ome_default_args.update({'device_ids': [25011, 25012], 'group_id': 1234, 'device_service_tags': [Constants.service_tag1]})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == 'parameters are mutually exclusive: device_ids|device_service_tags|ip_addresses'

    def test_ome_device_group_argument_exception_case3(self, ome_default_args):
        ome_default_args.update({'device_ids': [25011, 25012]})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == 'one of the following is required: name, group_id'

    def test_ome_device_group_argument_exception_case4(self, ome_default_args):
        ome_default_args.update({'group_id': 1234})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == 'one of the following is required: device_ids, device_service_tags, ip_addresses'

    def test_ome_device_group_argument_exception_case5(self, ome_default_args):
        ome_default_args.update({'device_ids': None, 'group_id': 1234, 'device_service_tags': None})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == 'parameters are mutually exclusive: device_ids|device_service_tags|ip_addresses'

    @pytest.mark.parametrize('exc_type', [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_device_group_argument_main_exception_failure_case(self, exc_type, mocker, ome_default_args, ome_connection_mock_for_device_group, ome_response_mock):
        ome_default_args.update({'name': 'Storage Services', 'device_ids': [25011, 25012]})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({'info': 'error_details'}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_group_id', side_effect=exc_type('url open error'))
            result = self._run_module(ome_default_args)
            assert result['unreachable'] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'get_group_id', side_effect=exc_type('exception message'))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_group_id', side_effect=exc_type('http://testhost.com', 400, 'http error message', {'accept-type': 'application/json'}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result

    @pytest.mark.parametrize('inp', [{'TypeId': 3000, 'MembershipTypeId': 24}, {'TypeId': 1000, 'MembershipTypeId': 24}, {'TypeId': 2000, 'MembershipTypeId': 12}])
    def test_validate_group_case01(self, inp, ome_response_mock):
        group_resp = {'Id': 25011, 'CreatedBy': 'user', 'TypeId': inp['TypeId'], 'MembershipTypeId': inp['MembershipTypeId']}
        f_module = self.get_module_mock(params={'name': 'group1', 'device_ids': [25011]})
        with pytest.raises(Exception) as exc:
            self.module.validate_group(group_resp, f_module, 'name', 'group1')
        assert exc.value.args[0] == ADD_STATIC_GROUP_MESSAGE

    @pytest.mark.parametrize('inp', [{'TypeId': 3000, 'MembershipTypeId': 24}, {'TypeId': 1000, 'MembershipTypeId': 24}, {'TypeId': 2000, 'MembershipTypeId': 12}])
    def test_validate_group_case02(self, inp, ome_response_mock):
        group_resp = {'Id': 25011, 'CreatedBy': 'user', 'TypeId': inp['TypeId'], 'MembershipTypeId': inp['MembershipTypeId']}
        f_module = self.get_module_mock(params={'name': 'group1', 'device_ids': [25011], 'state': 'absent'})
        with pytest.raises(Exception) as exc:
            self.module.validate_group(group_resp, f_module, 'name', 'group1')
        assert exc.value.args[0] == REMOVE_STATIC_GROUP_MESSAGE

    @pytest.mark.parametrize('inp,out', [(['192.168.2.0'], [IPAddress('192.168.2.0')]), (['fe80::ffff:ffff:ffff:ffff'], [IPAddress('fe80::ffff:ffff:ffff:ffff')]), (['192.168.2.0/24'], [IPNetwork('192.168.2.0/24')]), (['fe80::ffff:ffff:ffff:1111-fe80::ffff:ffff:ffff:ffff'], [IPRange('fe80::ffff:ffff:ffff:1111', 'fe80::ffff:ffff:ffff:ffff')]), (['192.168.2.0', 'fe80::ffff:ffff:ffff:ffff', '192.168.2.0/24', 'fe80::ffff:ffff:ffff:1111-fe80::ffff:ffff:ffff:ffff', '2002:c000:02e6::1/48'], [IPAddress('192.168.2.0'), IPAddress('fe80::ffff:ffff:ffff:ffff'), IPNetwork('192.168.2.0/24'), IPRange('fe80::ffff:ffff:ffff:1111', 'fe80::ffff:ffff:ffff:ffff'), IPNetwork('2002:c000:02e6::1/48')])])
    def test_get_all_ips_success_case(self, inp, out):
        f_module = self.get_module_mock(params={'name': 'group1', 'ip_addresses': inp})
        res = self.module.get_all_ips(inp, f_module)
        assert res == out

    @pytest.mark.parametrize('inp', [['abc'], [''], ['266.128'], ['100:1bcd:xyz'], ['192.168.0.0--192.168.0.1'], ['-192.168.0.0-192.168.0.1'], ['-192.168.0.0192.168.0.1'], ['192.168.0.0-192.168.0.1-'], ['192.168.0.0192.168.0.1-'], ['192.168.0.1//24'], ['\x0192.168.0.1//24'], ['192.168.0.1/\x14'], ['/192.168.0.1/24'], ['1.12.1.36/255.255.255.88']], ids=['abc', '', '266.128', '100:1bcd:xyz', '192.168.0.0--192.168.0.1', '-192.168.0.0-192.168.0.1', '-192.168.0.0192.168.0.1', '192.168.0.0-192.168.0.1-', '192.168.0.0192.168.0.1-', '192.168.0.1//24', '\x0192.168.0.1//24', '192.168.0.1/\x14', '/192.168.0.1/24', '1.12.1.36/255.255.255.88'])
    def test_get_all_ips_failure_case(self, inp):
        f_module = self.get_module_mock(params={'name': 'group1', 'ip_addresses': inp})
        with pytest.raises(Exception, match=INVALID_IP_FORMAT.format(inp[0])) as err:
            self.module.get_all_ips(inp, f_module)

    def test_get_device_id_from_ip_success_case(self):
        device_list = [{'Id': 1111, 'Identifier': 'device1', 'DeviceServiceTag': 'device1', 'DeviceManagement': [{'NetworkAddress': '192.168.2.255'}]}, {'Id': 2222, 'Identifier': 'device2', 'DeviceServiceTag': 'device2', 'DeviceManagement': [{'NetworkAddress': '192.168.4.10'}]}, {'Id': 3333, 'Identifier': 'device3', 'DeviceServiceTag': 'device3', 'DeviceManagement': [{'NetworkAddress': '192.168.2.10'}]}, {'Id': 4444, 'Identifier': 'device4', 'DeviceServiceTag': 'device4', 'DeviceManagement': [{'NetworkAddress': '192.168.3.10'}]}, {'Id': 5555, 'Identifier': 'device5', 'DeviceServiceTag': 'device5', 'DeviceManagement': [{'NetworkAddress': '192.168.4.3'}]}, {'Id': 6666, 'Identifier': 'device6', 'DeviceServiceTag': 'device6', 'DeviceManagement': [{'NetworkAddress': '192.168.3.11'}]}, {'Id': 7777, 'Identifier': 'device7', 'DeviceServiceTag': 'device7', 'DeviceManagement': [{'NetworkAddress': '192.168.3.0'}]}, {'Id': 8888, 'Identifier': 'device8', 'DeviceServiceTag': 'device8', 'DeviceManagement': [{'NetworkAddress': '192.168.4.1'}]}, {'Id': 9999, 'Identifier': 'device9', 'DeviceServiceTag': 'device9', 'DeviceManagement': [{'NetworkAddress': '192.168.4.5'}]}, {'Id': 1010, 'Identifier': 'device10', 'DeviceServiceTag': 'device10', 'DeviceManagement': [{'NetworkAddress': '192.168.4.9'}]}, {'Id': 1011, 'Identifier': 'device11', 'DeviceServiceTag': 'device11', 'DeviceManagement': [{'NetworkAddress': '[fe80::de0:b6b3:a764:0]'}]}, {'Id': 1012, 'Identifier': 'device11', 'DeviceServiceTag': 'device11', 'DeviceManagement': [{'NetworkAddress': '[fe90::de0:b6b3:a764:0]'}]}]
        output = {3333: '192.168.2.10', 4444: '192.168.3.10', 5555: '192.168.4.3', 6666: '192.168.3.11', 7777: '192.168.3.0', 8888: '192.168.4.1', 9999: '192.168.4.5', 1010: '192.168.4.9', 1011: 'fe80::de0:b6b3:a764:0'}
        ip_addresses = [IPNetwork('::ffff:192.168.2.0/125'), IPAddress('192.168.2.10'), IPAddress('fe80::ffff:ffff:ffff:ffff'), IPNetwork('fe80::ffff:ffff:ffff:ffff/24'), IPNetwork('192.168.3.0/24'), IPRange('192.168.4.1', '192.168.4.9')]
        f_module = self.get_module_mock(params={'name': 'group1', 'ip_addresses': ['::ffff:192.168.2.0/125', '192.168.2.10', 'fe80::ffff:ffff:ffff:ffff', '192.168.3.0/24', '192.168.4.1-192.168.4.9', 'fe80::ffff:ffff:ffff:ffff/24']})
        res = self.module.get_device_id_from_ip(ip_addresses, device_list, f_module)
        assert res == output

    def test_get_device_id_from_ip_failure_case(self):
        device_list = [{'Id': 1111, 'Identifier': 'device1', 'DeviceServiceTag': 'device1', 'DeviceManagement': [{'NetworkAddress': '192.168.2.255'}]}]
        ip_addresses = [IPNetwork('::ffff:192.168.2.0/125'), IPAddress('192.168.2.10'), IPAddress('fe80::ffff:ffff:ffff:ffff'), IPNetwork('fe80::ffff:ffff:ffff:ffff/24'), IPNetwork('192.168.3.0/24'), IPRange('192.168.4.1', '192.168.4.9')]
        with pytest.raises(Exception, match=IP_NOT_EXISTS):
            f_module = self.get_module_mock(params={'name': 'group1', 'ip_addresses': ['::ffff:192.168.2.0/125', '192.168.2.10', 'fe80::ffff:ffff:ffff:ffff', '192.168.3.0/24', '192.168.4.1-192.168.4.9', 'fe80::ffff:ffff:ffff:ffff/24']})
            self.module.get_device_id_from_ip(ip_addresses, device_list, f_module)

    def test_add_member_to_group_checkmode_case01(self, ome_connection_mock_for_device_group, ome_response_mock):
        report_list = [{'Id': 3333, 'DeviceServiceTag': 'device1', 'DeviceManagement': [{'NetworkAddress': '192.168.2.10'}]}, {'Id': 1013, 'DeviceServiceTag': 'device1', 'DeviceManagement': [{'NetworkAddress': '192.168.5.10'}]}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {'report_list': report_list}
        f_module = self.get_module_mock(params={'name': 'group1', 'ip_addresses': ['::ffff:192.168.2.0/125', '192.168.2.10', 'fe80::ffff:ffff:ffff:ffff', '192.168.3.0/24', '192.168.4.1-192.168.4.9', 'fe80::ffff:ffff:ffff:ffff/24']}, check_mode=True)
        device_id = {3333: '192.168.2.10', 4444: '192.168.3.10', 5555: '192.168.4.3', 1011: 'fe80::de0:b6b3:a764:0'}
        with pytest.raises(Exception, match='Changes found to be applied.'):
            self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group, 1, device_id, 'IPAddresses')

    def test_add_member_to_group_checkmode_case02(self, ome_connection_mock_for_device_group, ome_response_mock):
        report_list = [{'Id': 3333, 'DeviceServiceTag': 'device1', 'DeviceManagement': [{'NetworkAddress': '192.168.2.10'}]}, {'Id': 1013, 'DeviceServiceTag': 'device1', 'DeviceManagement': [{'NetworkAddress': '192.168.5.10'}]}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {'report_list': report_list}
        f_module = self.get_module_mock(params={'name': 'group1', 'ip_addresses': ['192.168.2.10']}, check_mode=True)
        device_id = {3333: '192.168.2.10'}
        with pytest.raises(Exception, match='No changes found to be applied.'):
            self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group, 1, device_id, 'IPAddresses')

    def test_add_member_to_group_idempotency_case(self, ome_connection_mock_for_device_group, ome_response_mock):
        report_list = [{'Id': 3333, 'DeviceServiceTag': 'device1', 'DeviceManagement': [{'NetworkAddress': '192.168.2.10'}]}, {'Id': 1013, 'DeviceServiceTag': 'device1', 'DeviceManagement': [{'NetworkAddress': '192.168.5.10'}]}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {'report_list': report_list}
        f_module = self.get_module_mock(params={'name': 'group1', 'ip_addresses': ['192.168.2.10']})
        device_id = {3333: '192.168.2.10'}
        with pytest.raises(Exception) as exc:
            self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group, 1, device_id, 'IPAddresses')
        assert exc.value.args[0] == 'No changes found to be applied.'

    def test_ome_device_group_main_ip_address_case(self, ome_connection_mock_for_device_group, mocker, ome_response_mock, ome_default_args):
        ome_default_args.update({'name': 'Storage Services', 'ip_addresses': ['192.168.2.10']})
        ome_response_mock.status_code = 204
        ome_response_mock.success = True
        mocker.patch(MODULE_PATH + 'get_group_id', return_value=1)
        mocker.patch(MODULE_PATH + 'get_device_id', return_value=[25011, 25012])
        mocker.patch(MODULE_PATH + 'add_member_to_group', return_value=(ome_response_mock, ['192.168.2.10']))
        result = self._run_module(ome_default_args)
        assert result['msg'] == 'Successfully added member(s) to the device group.'
        assert result['ip_addresses_added'] == ['192.168.2.10']

    def test_get_device_id_ip_address_case(self, ome_connection_mock_for_device_group, mocker):
        f_module = self.get_module_mock(params={'name': 'group1', 'ip_addresses': ['192.168.2.10']})
        mocker.patch(MODULE_PATH + 'get_all_ips', return_value=[IPAddress('192.168.2.10')])
        mocker.patch(MODULE_PATH + 'get_device_id_from_ip', return_value={1111: '192.168.2.10'})
        (each_device_list, key) = self.module.get_device_id(ome_connection_mock_for_device_group, f_module)
        assert key == 'IPAddresses'
        assert each_device_list == {1111: '192.168.2.10'}

    def test_get_current_member_of_group(self, ome_connection_mock_for_device_group, ome_response_mock):
        report_list = [{'Id': 3333, 'DeviceServiceTag': 'device1', 'DeviceManagement': [{'NetworkAddress': '192.168.2.10'}]}, {'Id': 1013, 'DeviceServiceTag': 'device1', 'DeviceManagement': [{'NetworkAddress': '192.168.5.10'}]}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {'report_list': report_list}
        group_id = 1011
        device_id_list = self.module.get_current_member_of_group(ome_connection_mock_for_device_group, group_id)
        assert device_id_list == [3333, 1013]

    def test_ome_device_group_remove_member_from_group(self, ome_connection_mock_for_device_group, ome_response_mock):
        report_list = [{'Id': 25011, 'DeviceServiceTag': 'SEFRG2'}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {'report_list': report_list}
        f_module = self.get_module_mock(params={'name': 'Storage Services', 'device_ids': [25011], 'state': 'absent'})
        group_id = 1011
        device_ids = [25011]
        current_device_list = [25011]
        ome_response_mock.status_code = 204
        ome_response_mock.success = True
        resp = self.module.remove_member_from_group(f_module, ome_connection_mock_for_device_group, group_id, device_ids, current_device_list)
        assert resp.status_code == 204
        f_module.check_mode = True
        with pytest.raises(Exception, match='Changes found to be applied.') as exc:
            self.module.remove_member_from_group(f_module, ome_connection_mock_for_device_group, group_id, device_ids, current_device_list)
        f_module.check_mode = False
        report_list = [{'Id': 25013, 'DeviceServiceTag': 'SEFRG4'}, {'Id': 25014, 'DeviceServiceTag': 'SEFRG5'}]
        device_ids = [10000, 24000, 25013, 12345, 25014]
        current_device_list = [25013, 25014]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {'report_list': report_list}
        resp = self.module.remove_member_from_group(f_module, ome_connection_mock_for_device_group, group_id, device_ids, current_device_list)
        assert resp.status_code == 204
        current_device_list = [25013, 25014]
        device_ids = [25011]
        f_module.check_mode = True
        with pytest.raises(Exception, match='No changes found to be applied.') as exc:
            self.module.remove_member_from_group(f_module, ome_connection_mock_for_device_group, group_id, device_ids, current_device_list)
        current_device_list = [25013, 25014]
        f_module.check_mode = False
        device_ids = []
        with pytest.raises(Exception, match='No changes found to be applied.') as exc:
            self.module.remove_member_from_group(f_module, ome_connection_mock_for_device_group, group_id, device_ids, current_device_list)

    def test_ome_device_group_main_absent_case(self, ome_connection_mock_for_device_group, mocker, ome_response_mock, ome_default_args):
        ome_default_args.update({'name': 'Storage Services', 'device_ids': [25011, 25012], 'state': 'absent'})
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        mocker.patch(MODULE_PATH + 'get_group_id', return_value=1)
        mocker.patch(MODULE_PATH + 'get_device_id', return_value=[25011, 25012])
        mocker.patch(MODULE_PATH + 'get_current_member_of_group', return_value=[25011, 25012])
        mocker.patch(MODULE_PATH + 'remove_member_from_group', return_value=ome_response_mock)
        result = self._run_module(ome_default_args)
        assert result['msg'] == 'Successfully removed member(s) from the device group.'