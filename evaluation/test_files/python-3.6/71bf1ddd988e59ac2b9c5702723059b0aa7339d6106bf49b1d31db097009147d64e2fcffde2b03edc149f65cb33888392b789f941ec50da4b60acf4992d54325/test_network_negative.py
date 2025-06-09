from infiniguard_api.lib.rest.common import http_code
import os
import json
import unittest
import mock
import ddt
from infiniguard_api.api_server.infiniguard_api_app import infiniguard_api_app
from infiniguard_api.lib.iguard_api_exceptions import IguardApiWithCodeException

@ddt.ddt
class TestVerifyNetwork(unittest.TestCase):
    log_tests = False

    @classmethod
    def setUpClass(cls):
        super(TestVerifyNetwork, cls).setUpClass()
        try:
            cls.app = infiniguard_api_app.test_client()
        except Exception as e:
            cls.tearDownClass()
            raise e

    @classmethod
    def tearDownClass(cls):
        pass

    def shortDescription(self):
        return None

    def setUp(self):
        super(TestVerifyNetwork, self).setUp()
        self.base = '/network'
        self.session = self.__class__.app.session_transaction()
        self.host_create_request = {'hostname': 'dde2-2371', 'search_domain': 'localdomain', 'dns_servers': ['172.16.0.10'], 'default_gateway': '10.10.1.1'}
        self.static_route_create_request = {'network': '10.10.10.0', 'mask': '255.255.255.0', 'gateway': '10.10.10.1'}

    def tearDown(self):
        pass

    @ddt.file_data('create.json')
    def test10CreateCliException(self, parms):
        (request, obj) = parms
        with mock.patch('infiniguard_api.controller.network.{}.run_syscli1'.format(obj)) as mocked_syscli:
            mocked_syscli.side_effect = Exception()
            rv = self.__class__.app.post('{}/{}/'.format(self.base, obj), data=json.dumps(request), content_type='application/json')
        self.assertEqual(rv.status_code, http_code.INTERNAL_SERVER_ERROR)
        resp = json.loads(rv.data)
        self.assertEqual(resp['error']['code'], 'UNEXPECTED_EXCEPTION')
        self.assertTrue(isinstance(resp['error']['message'], list))

    @ddt.file_data('create.json')
    def test10CreateCliError(self, parms):
        (request, obj) = parms
        with mock.patch('infiniguard_api.controller.network.{}.run_syscli1'.format(obj)) as mocked_syscli:
            mocked_syscli.return_value = (None, 'HAHA')
            rv = self.__class__.app.post('{}/{}/'.format(self.base, obj), data=json.dumps(request), content_type='application/json')
        self.assertEqual(rv.status_code, http_code.INTERNAL_SERVER_ERROR)
        resp = json.loads(rv.data)
        self.assertEqual(resp['error']['code'], 'SYSTEM_ERROR')
        self.assertTrue(isinstance(resp['error']['message'], list))

    @ddt.data('host', 'static_routes', 'interfaces')
    def test10GetCliException(self, obj):
        with mock.patch('infiniguard_api.controller.network.{}.run_syscli1'.format(obj)) as mocked_syscli:
            mocked_syscli.side_effect = Exception()
            rv = self.__class__.app.get('{}/{}/'.format(self.base, obj), content_type='application/json')
        self.assertEqual(rv.status_code, http_code.INTERNAL_SERVER_ERROR)
        resp = json.loads(rv.data)
        self.assertEqual(resp['error']['code'], 'UNEXPECTED_EXCEPTION')
        self.assertTrue(isinstance(resp['error']['message'], list))

    @ddt.data('host', 'static_routes', 'interfaces')
    def test10GetCliError(self, obj):
        with mock.patch('infiniguard_api.controller.network.{}.run_syscli1'.format(obj)) as mocked_syscli:
            mocked_syscli.return_value = (None, 'HAHA')
            rv = self.__class__.app.get('{}/{}/'.format(self.base, obj), content_type='application/json')
        self.assertEqual(rv.status_code, http_code.INTERNAL_SERVER_ERROR)
        resp = json.loads(rv.data)
        self.assertEqual(resp['error']['code'], 'SYSTEM_ERROR')
        self.assertTrue(isinstance(resp['error']['message'], list))
if __name__ == '__main__':
    unittest.main()