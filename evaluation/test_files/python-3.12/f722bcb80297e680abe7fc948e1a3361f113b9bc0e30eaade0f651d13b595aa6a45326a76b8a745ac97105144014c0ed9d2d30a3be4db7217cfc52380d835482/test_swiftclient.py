import gzip
import json
import logging
import io
import socket
import string
import unittest
from unittest import mock
import warnings
import tempfile
from hashlib import md5
from urllib.parse import urlparse
from requests.exceptions import RequestException
from .utils import MockHttpTest, fake_get_auth_keystone, StubResponse, FakeKeystone
from swiftclient.utils import EMPTY_ETAG
from swiftclient.exceptions import ClientException
from swiftclient import client as c
import swiftclient.utils
import swiftclient

class TestClientException(unittest.TestCase):

    def test_is_exception(self):
        self.assertTrue(issubclass(c.ClientException, Exception))

    def test_format(self):
        exc = c.ClientException('something failed')
        self.assertIn('something failed', str(exc))
        test_kwargs = ('scheme', 'host', 'port', 'path', 'query', 'status', 'reason', 'device', 'response_content')
        for value in test_kwargs:
            kwargs = {'http_%s' % value: value}
            exc = c.ClientException('test', **kwargs)
            self.assertIn(value, str(exc))

    def test_attrs(self):
        test_kwargs = ('scheme', 'host', 'port', 'path', 'query', 'status', 'reason', 'device', 'response_content', 'response_headers')
        for value in test_kwargs:
            key = 'http_%s' % value
            kwargs = {key: value}
            exc = c.ClientException('test', **kwargs)
            self.assertIs(True, hasattr(exc, key))
            self.assertEqual(getattr(exc, key), value)

    def test_transaction_id_from_headers(self):
        exc = c.ClientException('test')
        self.assertIsNone(exc.transaction_id)
        exc = c.ClientException('test', http_response_headers={})
        self.assertIsNone(exc.transaction_id)
        exc = c.ClientException('test', http_response_headers={'X-Trans-Id': 'some-id'})
        self.assertEqual(exc.transaction_id, 'some-id')
        self.assertIn('(txn: some-id)', str(exc))
        exc = c.ClientException('test', http_response_headers={'X-Openstack-Request-Id': 'some-other-id'})
        self.assertEqual(exc.transaction_id, 'some-other-id')
        self.assertIn('(txn: some-other-id)', str(exc))

class MockHttpResponse:

    def __init__(self, status=0, headers=None, verify=False):
        self.status = status
        self.status_code = status
        self.reason = 'OK'
        self.buffer = []
        self.requests_params = None
        self.verify = verify
        self.md5sum = md5()
        self.headers = {'etag': '"%s"' % EMPTY_ETAG}
        if headers:
            self.headers.update(headers)
        self.closed = False

        class Raw:

            def __init__(self, headers):
                self.headers = headers

            def read(self, **kw):
                return ''

            def getheader(self, name, default):
                return self.headers.get(name, default)
        self.raw = Raw(headers)

    def read(self):
        return ''

    def close(self):
        self.closed = True

    def getheader(self, name, default):
        return self.headers.get(name, default)

    def getheaders(self):
        return dict(self.headers).items()

    def fake_response(self):
        return self

    def _fake_request(self, *arg, **kwarg):
        self.status = 200
        self.requests_params = kwarg
        if self.verify:
            for chunk in kwarg['data']:
                self.md5sum.update(chunk)
        for k, v in kwarg['headers'].items():
            self.buffer.append((k, v))
        return self.fake_response()

class TestHttpHelpers(MockHttpTest):

    def test_quote(self):
        value = b'bytes\xff'
        self.assertEqual('bytes%FF', c.quote(value))
        value = 'native string'
        self.assertEqual('native%20string', c.quote(value))
        value = 'unicode string'
        self.assertEqual('unicode%20string', c.quote(value))
        value = 'unicode:é€'
        self.assertEqual('unicode%3A%C3%A9%E2%82%AC', c.quote(value))

    def test_parse_header_string(self):
        value = b'bytes'
        self.assertEqual('bytes', c.parse_header_string(value))
        value = 'unicode:é€'
        self.assertEqual('unicode:é€', c.parse_header_string(value))
        value = 'native%20string'
        self.assertEqual('native string', c.parse_header_string(value))
        value = b'encoded%20bytes%E2%82%AC'
        self.assertEqual('encoded bytes€', c.parse_header_string(value))
        value = 'encoded%20unicode%E2%82%AC'
        self.assertEqual('encoded unicode€', c.parse_header_string(value))
        value = b'bad%20bytes%ff%E2%82%AC'
        self.assertEqual('bad%20bytes%ff%E2%82%AC', c.parse_header_string(value))
        value = 'bad%20unicode%ff€'
        self.assertEqual('bad%20unicode%ff€', c.parse_header_string(value))
        value = b'really%20bad\xffbytes'
        self.assertEqual('really%2520bad%FFbytes', c.parse_header_string(value))

    def test_http_connection(self):
        url = 'http://www.test.com'
        _junk, conn = c.http_connection(url)
        self.assertIs(type(conn), c.HTTPConnection)
        url = 'https://www.test.com'
        _junk, conn = c.http_connection(url)
        self.assertIs(type(conn), c.HTTPConnection)
        url = 'ftp://www.test.com'
        self.assertRaises(c.ClientException, c.http_connection, url)

    def test_encode_meta_headers(self):
        headers = {'abc': '123', 'x-container-meta-Δ': 123, 'x-account-meta-Δ': 12.3, 'x-object-meta-Δ': True}
        r = swiftclient.encode_meta_headers(headers)
        self.assertEqual(len(headers), len(r))
        self.assertIs(type(r.get('abc')), bytes)
        del r['abc']
        for k, v in r.items():
            self.assertIs(type(k), bytes)
            self.assertIs(type(v), bytes)
            self.assertIn(v, (b'123', b'12.3', b'True'))

    def test_set_user_agent_default(self):
        _junk, conn = c.http_connection('http://www.example.com')
        req_headers = {}

        def my_request_handler(*a, **kw):
            req_headers.update(kw.get('headers', {}))
        conn._request = my_request_handler
        conn.request('GET', '/')
        ua = req_headers.get('user-agent', 'XXX-MISSING-XXX')
        self.assertTrue(ua.startswith('python-swiftclient-'))

    def test_set_user_agent_per_request_override(self):
        _junk, conn = c.http_connection('http://www.example.com')
        req_headers = {}

        def my_request_handler(*a, **kw):
            req_headers.update(kw.get('headers', {}))
        conn._request = my_request_handler
        conn.request('GET', '/', headers={'User-Agent': 'Me'})
        ua = req_headers.get('user-agent', 'XXX-MISSING-XXX')
        self.assertEqual(ua, b'Me', req_headers)

    def test_set_user_agent_default_override(self):
        _junk, conn = c.http_connection('http://www.example.com', default_user_agent='a-new-default')
        req_headers = {}

        def my_request_handler(*a, **kw):
            req_headers.update(kw.get('headers', {}))
        conn._request = my_request_handler
        conn._request = my_request_handler
        conn.request('GET', '/')
        ua = req_headers.get('user-agent', 'XXX-MISSING-XXX')
        self.assertEqual(ua, 'a-new-default')

class TestGetAuth(MockHttpTest):

    def test_ok(self):
        c.http_connection = self.fake_http_connection(200)
        url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf')
        self.assertIsNone(url)
        self.assertIsNone(token)

    def test_invalid_auth(self):
        self.assertRaises(c.ClientException, c.get_auth, 'http://www.tests.com', 'asdf', 'asdf', auth_version='foo')

    def test_auth_v1(self):
        c.http_connection = self.fake_http_connection(200, auth_v1=True)
        url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf', auth_version='1.0')
        self.assertEqual(url, 'storageURL')
        self.assertEqual(token, 'someauthtoken')

    def test_auth_v1_insecure(self):
        c.http_connection = self.fake_http_connection(200, 200, auth_v1=True)
        url, token = c.get_auth('http://www.test.com/invalid_cert', 'asdf', 'asdf', auth_version='1.0', insecure=True)
        self.assertEqual(url, 'storageURL')
        self.assertEqual(token, 'someauthtoken')
        with self.assertRaises(c.ClientException) as exc_context:
            c.get_auth('http://www.test.com/invalid_cert', 'asdf', 'asdf', auth_version='1.0')
        self.assertIn('invalid_certificate', str(exc_context.exception))

    def test_auth_v1_timeout(self):
        orig_http_connection = c.http_connection
        timeouts = []

        def fake_request_handler(*a, **kw):
            if 'timeout' in kw:
                timeouts.append(kw['timeout'])
            else:
                timeouts.append(None)
            return MockHttpResponse(status=200, headers={'x-auth-token': 'a_token', 'x-storage-url': 'http://files.example.com/v1/AUTH_user'})

        def fake_connection(*a, **kw):
            url, conn = orig_http_connection(*a, **kw)
            conn._request = fake_request_handler
            return (url, conn)
        with mock.patch('swiftclient.client.http_connection', fake_connection):
            c.get_auth('http://www.test.com', 'asdf', 'asdf', auth_version='1.0', timeout=42.0)
            c.get_auth('http://www.test.com', 'asdf', 'asdf', auth_version='1.0', timeout=None)
            c.get_auth('http://www.test.com', 'asdf', 'asdf', auth_version='1.0')
        self.assertEqual(timeouts, [42.0, None, None])

    def test_auth_v2_timeout(self):
        fake_ks = FakeKeystone(endpoint='http://some_url', token='secret')
        with mock.patch('swiftclient.client.ksclient_v2', fake_ks):
            c.get_auth('http://www.test.com', 'asdf', 'asdf', os_options=dict(tenant_name='tenant'), auth_version='2.0', timeout=42.0)
            c.get_auth('http://www.test.com', 'asdf', 'asdf', os_options=dict(tenant_name='tenant'), auth_version='2.0', timeout=None)
            c.get_auth('http://www.test.com', 'asdf', 'asdf', os_options=dict(tenant_name='tenant'), auth_version='2.0')
        self.assertEqual(3, len(fake_ks.calls))
        timeouts = [call['timeout'] for call in fake_ks.calls]
        self.assertEqual([42.0, None, None], timeouts)

    def test_auth_v2_with_tenant_name(self):
        os_options = {'tenant_name': 'asdf'}
        req_args = {'auth_version': '2.0'}
        ks = fake_get_auth_keystone(os_options, required_kwargs=req_args)
        with mock.patch('swiftclient.client.get_auth_keystone', ks):
            url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_auth_v2_with_tenant_id(self):
        os_options = {'tenant_id': 'asdf'}
        req_args = {'auth_version': '2.0'}
        ks = fake_get_auth_keystone(os_options, required_kwargs=req_args)
        with mock.patch('swiftclient.client.get_auth_keystone', ks):
            url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_auth_v2_with_project_name(self):
        os_options = {'project_name': 'asdf'}
        req_args = {'auth_version': '2.0'}
        ks = fake_get_auth_keystone(os_options, required_kwargs=req_args)
        with mock.patch('swiftclient.client.get_auth_keystone', ks):
            url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_auth_v2_with_project_id(self):
        os_options = {'project_id': 'asdf'}
        req_args = {'auth_version': '2.0'}
        ks = fake_get_auth_keystone(os_options, required_kwargs=req_args)
        with mock.patch('swiftclient.client.get_auth_keystone', ks):
            url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_auth_v2_no_tenant_name_or_tenant_id(self):
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone({})):
            self.assertRaises(c.ClientException, c.get_auth, 'http://www.tests.com', 'asdf', 'asdf', os_options={}, auth_version='2.0')

    def test_auth_v2_with_tenant_name_none_and_tenant_id_none(self):
        os_options = {'tenant_name': None, 'tenant_id': None}
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone(os_options)):
            self.assertRaises(c.ClientException, c.get_auth, 'http://www.tests.com', 'asdf', 'asdf', os_options=os_options, auth_version='2.0')

    def test_auth_v2_with_tenant_user_in_user(self):
        tenant_option = {'tenant_name': 'foo'}
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone(tenant_option)):
            url, token = c.get_auth('http://www.test.com', 'foo:bar', 'asdf', os_options={}, auth_version='2.0')
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_auth_v2_tenant_name_no_os_options(self):
        tenant_option = {'tenant_name': 'asdf'}
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone(tenant_option)):
            url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf', tenant_name='asdf', os_options={}, auth_version='2.0')
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_auth_v2_with_os_options(self):
        os_options = {'service_type': 'object-store', 'endpoint_type': 'internalURL', 'tenant_name': 'asdf'}
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone(os_options)):
            url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_auth_v2_with_tenant_user_in_user_no_os_options(self):
        tenant_option = {'tenant_name': 'foo'}
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone(tenant_option)):
            url, token = c.get_auth('http://www.test.com', 'foo:bar', 'asdf', auth_version='2.0')
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_auth_v2_with_os_region_name(self):
        os_options = {'region_name': 'good-region', 'tenant_name': 'asdf'}
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone(os_options)):
            url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_auth_v2_no_endpoint(self):
        os_options = {'region_name': 'unknown_region', 'tenant_name': 'asdf'}
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone(os_options, c.ClientException)):
            self.assertRaises(c.ClientException, c.get_auth, 'http://www.tests.com', 'asdf', 'asdf', os_options=os_options, auth_version='2.0')

    def test_auth_v2_ks_exception(self):
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone({}, c.ClientException)):
            self.assertRaises(c.ClientException, c.get_auth, 'http://www.tests.com', 'asdf', 'asdf', os_options={}, auth_version='2.0')

    def test_auth_v2_cacert(self):
        os_options = {'tenant_name': 'foo'}
        auth_url_secure = 'https://www.tests.com'
        auth_url_insecure = 'https://www.tests.com/self-signed-certificate'
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone(os_options, None)):
            url, token = c.get_auth(auth_url_secure, 'asdf', 'asdf', os_options=os_options, auth_version='2.0', insecure=False)
            self.assertTrue(url.startswith('http'))
            self.assertTrue(token)
            url, token = c.get_auth(auth_url_insecure, 'asdf', 'asdf', os_options=os_options, auth_version='2.0', cacert='ca.pem', insecure=False)
            self.assertTrue(url.startswith('http'))
            self.assertTrue(token)
            self.assertRaises(c.ClientException, c.get_auth, auth_url_insecure, 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
            self.assertRaises(c.ClientException, c.get_auth, auth_url_insecure, 'asdf', 'asdf', os_options=os_options, auth_version='2.0', insecure=False)

    def test_auth_v2_insecure(self):
        os_options = {'tenant_name': 'foo'}
        auth_url_secure = 'https://www.tests.com'
        auth_url_insecure = 'https://www.tests.com/invalid-certificate'
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone(os_options, None)):
            url, token = c.get_auth(auth_url_secure, 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
            self.assertTrue(url.startswith('http'))
            self.assertTrue(token)
            url, token = c.get_auth(auth_url_insecure, 'asdf', 'asdf', os_options=os_options, auth_version='2.0', insecure=True)
            self.assertTrue(url.startswith('http'))
            self.assertTrue(token)
            self.assertRaises(c.ClientException, c.get_auth, auth_url_insecure, 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
            self.assertRaises(c.ClientException, c.get_auth, auth_url_insecure, 'asdf', 'asdf', os_options=os_options, auth_version='2.0', insecure=False)

    def test_auth_v2_cert(self):
        os_options = {'tenant_name': 'foo'}
        auth_url_no_sslauth = 'https://www.tests.com'
        auth_url_sslauth = 'https://www.tests.com/client-certificate'
        with mock.patch('swiftclient.client.get_auth_keystone', fake_get_auth_keystone(os_options, None)):
            url, token = c.get_auth(auth_url_no_sslauth, 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
            self.assertTrue(url.startswith('http'))
            self.assertTrue(token)
            url, token = c.get_auth(auth_url_sslauth, 'asdf', 'asdf', os_options=os_options, auth_version='2.0', cert='minnie', cert_key='mickey')
            self.assertTrue(url.startswith('http'))
            self.assertTrue(token)
            self.assertRaises(c.ClientException, c.get_auth, auth_url_sslauth, 'asdf', 'asdf', os_options=os_options, auth_version='2.0')
            self.assertRaises(c.ClientException, c.get_auth, auth_url_sslauth, 'asdf', 'asdf', os_options=os_options, auth_version='2.0', cert='minnie')

    def test_auth_v3_with_tenant_name(self):
        os_options = {'tenant_name': 'asdf'}
        req_args = {'auth_version': '3'}
        ks = fake_get_auth_keystone(os_options, required_kwargs=req_args)
        with mock.patch('swiftclient.client.get_auth_keystone', ks):
            url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf', os_options=os_options, auth_version='3')
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_auth_v3applicationcredential(self):
        from keystoneauth1 import exceptions as ksauthexceptions
        os_options = {'auth_type': 'v3applicationcredential', 'application_credential_id': 'proejct_id', 'application_credential_secret': 'secret'}

        class FakeEndpointData:
            catalog_url = 'http://swift.cluster/v1/KEY_project_id'

        class FakeKeystoneuth1v3Session:

            def __init__(self, auth):
                self.auth = auth
                self.token = 'token'

            def get_token(self):
                if self.auth.auth_url == 'http://keystone:5000/v3':
                    return self.token
                elif self.auth.auth_url == 'http://keystone:9000/v3':
                    raise ksauthexceptions.AuthorizationFailure
                else:
                    raise ksauthexceptions.Unauthorized

            def get_endpoint_data(self, service_type, endpoint_type, **kwargs):
                return FakeEndpointData()
        mock_sess = FakeKeystoneuth1v3Session
        with mock.patch('keystoneauth1.session.Session', mock_sess):
            url, token = c.get_auth('http://keystone:5000', '', '', os_options=os_options, auth_version='3')
        self.assertTrue(url.startswith('http'))
        self.assertEqual(url, 'http://swift.cluster/v1/KEY_project_id')
        self.assertEqual(token, 'token')
        with mock.patch('keystoneauth1.session.Session', mock_sess):
            with self.assertRaises(c.ClientException) as exc_mgr:
                url, token = c.get_auth('http://keystone:9000', '', '', os_options=os_options, auth_version='3')
        body = 'Unauthorized. Check application credential id and secret.'
        body = 'Authorization Failure. Cannot authorize API client.'
        self.assertEqual(exc_mgr.exception.__str__()[-89:], body)
        with mock.patch('keystoneauth1.session.Session', mock_sess):
            with self.assertRaises(c.ClientException) as exc_mgr:
                url, token = c.get_auth('http://keystone:5000', '', '', os_options=os_options, auth_version='2')
        body = 'Unauthorized. Check application credential id and secret.'
        self.assertEqual(exc_mgr.exception.__str__()[-89:], body)

    def test_get_keystone_client_2_0(self):
        os_options = {'tenant_name': 'asdf'}
        req_args = {'auth_version': '2.0'}
        ks = fake_get_auth_keystone(os_options, required_kwargs=req_args)
        with mock.patch('swiftclient.client.get_auth_keystone', ks):
            url, token = c.get_keystoneclient_2_0('http://www.test.com', 'asdf', 'asdf', os_options=os_options)
        self.assertTrue(url.startswith('http'))
        self.assertTrue(token)

    def test_get_auth_keystone_versionless(self):
        fake_ks = FakeKeystone(endpoint='http://some_url', token='secret')
        with mock.patch('swiftclient.client.ksclient_v3', fake_ks):
            c.get_auth_keystone('http://authurl', 'user', 'key', {})
        self.assertEqual(1, len(fake_ks.calls))
        self.assertEqual('http://authurl/v3', fake_ks.calls[0].get('auth_url'))

    def test_get_auth_keystone_versionless_auth_version_set(self):
        fake_ks = FakeKeystone(endpoint='http://some_url', token='secret')
        with mock.patch('swiftclient.client.ksclient_v2', fake_ks):
            c.get_auth_keystone('http://auth_url', 'user', 'key', {}, auth_version='2.0')
        self.assertEqual(1, len(fake_ks.calls))
        self.assertEqual('http://auth_url/v2.0', fake_ks.calls[0].get('auth_url'))

    def test_get_auth_keystone_versionful(self):
        fake_ks = FakeKeystone(endpoint='http://some_url', token='secret')
        with mock.patch('swiftclient.client.ksclient_v3', fake_ks):
            c.get_auth_keystone('http://auth_url/v3', 'user', 'key', {}, auth_version='3')
        self.assertEqual(1, len(fake_ks.calls))
        self.assertEqual('http://auth_url/v3', fake_ks.calls[0].get('auth_url'))

    def test_get_auth_keystone_devstack_versionful(self):
        fake_ks = FakeKeystone(endpoint='http://storage.example.com/v1/AUTH_user', token='secret')
        with mock.patch('swiftclient.client.ksclient_v3', fake_ks):
            c.get_auth_keystone('https://192.168.8.8/identity/v3', 'user', 'key', {}, auth_version='3')
        self.assertEqual(1, len(fake_ks.calls))
        self.assertEqual('https://192.168.8.8/identity/v3', fake_ks.calls[0].get('auth_url'))

    def test_get_auth_keystone_devstack_versionless(self):
        fake_ks = FakeKeystone(endpoint='http://storage.example.com/v1/AUTH_user', token='secret')
        with mock.patch('swiftclient.client.ksclient_v3', fake_ks):
            c.get_auth_keystone('https://192.168.8.8/identity', 'user', 'key', {}, auth_version='3')
        self.assertEqual(1, len(fake_ks.calls))
        self.assertEqual('https://192.168.8.8/identity/v3', fake_ks.calls[0].get('auth_url'))

    def test_auth_keystone_url_some_junk_nonsense(self):
        fake_ks = FakeKeystone(endpoint='http://storage.example.com/v1/AUTH_user', token='secret')
        with mock.patch('swiftclient.client.ksclient_v3', fake_ks):
            c.get_auth_keystone('http://blah.example.com/v2moo', 'user', 'key', {}, auth_version='3')
        self.assertEqual(1, len(fake_ks.calls))
        self.assertEqual('http://blah.example.com/v2moo/v3', fake_ks.calls[0].get('auth_url'))

    def test_auth_with_session(self):
        mock_session = mock.MagicMock()
        mock_session.get_endpoint.return_value = 'http://storagehost/v1/acct'
        mock_session.get_token.return_value = 'token'
        url, token = c.get_auth('http://www.test.com', 'asdf', 'asdf', session=mock_session)
        self.assertEqual(url, 'http://storagehost/v1/acct')
        self.assertTrue(token)

class TestGetAccount(MockHttpTest):

    def test_no_content(self):
        c.http_connection = self.fake_http_connection(204)
        value = c.get_account('http://www.test.com/v1/acct', 'asdf')[1]
        self.assertEqual(value, [])
        self.assertRequests([('GET', '/v1/acct?format=json', '', {'accept-encoding': 'gzip', 'x-auth-token': 'asdf'})])

    def test_param_marker(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&marker=marker')
        c.get_account('http://www.test.com/v1/acct', 'asdf', marker='marker')
        self.assertRequests([('GET', '/v1/acct?format=json&marker=marker', '', {'accept-encoding': 'gzip', 'x-auth-token': 'asdf'})])

    def test_param_limit(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&limit=10')
        c.get_account('http://www.test.com/v1/acct', 'asdf', limit=10)
        self.assertRequests([('GET', '/v1/acct?format=json&limit=10', '', {'accept-encoding': 'gzip', 'x-auth-token': 'asdf'})])

    def test_param_prefix(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&prefix=asdf/')
        c.get_account('http://www.test.com/v1/acct', 'asdf', prefix='asdf/')
        self.assertRequests([('GET', '/v1/acct?format=json&prefix=asdf/', '', {'accept-encoding': 'gzip', 'x-auth-token': 'asdf'})])

    def test_param_end_marker(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&end_marker=end_marker')
        c.get_account('http://www.test.com/v1/acct', 'asdf', end_marker='end_marker')
        self.assertRequests([('GET', '/v1/acct?format=json&end_marker=end_marker', '', {'accept-encoding': 'gzip', 'x-auth-token': 'asdf'})])

    def test_param_delimiter(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&delimiter=-')
        c.get_account('http://www.test.com/v1/acct', 'asdf', delimiter='-')
        self.assertRequests([('GET', '/v1/acct?format=json&delimiter=-', '', {'accept-encoding': 'gzip', 'x-auth-token': 'asdf'})])

class TestHeadAccount(MockHttpTest):

    def test_ok(self):
        c.http_connection = self.fake_http_connection(200, headers={'x-account-meta-color': 'blue'})
        resp_headers = c.head_account('http://www.tests.com', 'asdf')
        self.assertEqual(resp_headers['x-account-meta-color'], 'blue')
        self.assertRequests([('HEAD', 'http://www.tests.com', '', {'x-auth-token': 'asdf'})])
        self.assertTrue(self.request_log[-1][-1]._closed)

    def test_server_error(self):
        body = 'c' * 65
        headers = {'foo': 'bar'}
        c.http_connection = self.fake_http_connection(StubResponse(500, body, headers))
        with self.assertRaises(c.ClientException) as exc_context:
            c.head_account('http://www.tests.com', 'asdf')
        e = exc_context.exception
        self.assertEqual(e.http_response_content, body)
        self.assertEqual(e.http_status, 500)
        self.assertRequests([('HEAD', 'http://www.tests.com', '', {'x-auth-token': 'asdf'})])
        new_body = '[first 60 chars of response] ' + body[0:60]
        self.assertEqual(e.__str__()[-89:], new_body)

class TestPostAccount(MockHttpTest):

    def test_ok(self):
        c.http_connection = self.fake_http_connection(200, headers={'X-Account-Meta-Color': 'blue'}, body='foo')
        headers = {'x-account-meta-shape': 'square'}
        resp_headers, body = c.post_account('http://www.tests.com/path/to/account', 'asdf', headers, query_string='bar=baz', data='some data')
        self.assertEqual('blue', resp_headers.get('x-account-meta-color'))
        self.assertEqual('foo', body)
        self.assertRequests([('POST', 'http://www.tests.com/path/to/account?bar=baz', 'some data', {'x-auth-token': 'asdf', 'x-account-meta-shape': 'square'})])
        self.assertEqual(headers, {'x-account-meta-shape': 'square'})

    def test_server_error(self):
        body = 'c' * 65
        c.http_connection = self.fake_http_connection(500, body=body)
        with self.assertRaises(c.ClientException) as exc_mgr:
            c.post_account('http://www.tests.com', 'asdf', {})
        self.assertEqual(exc_mgr.exception.http_response_content, body)
        self.assertEqual(exc_mgr.exception.http_status, 500)
        self.assertRequests([('POST', 'http://www.tests.com', None, {'x-auth-token': 'asdf'})])
        new_body = '[first 60 chars of response] ' + body[0:60]
        self.assertEqual(exc_mgr.exception.__str__()[-89:], new_body)

class TestGetContainer(MockHttpTest):

    def test_no_content(self):
        c.http_connection = self.fake_http_connection(204)
        value = c.get_container('http://www.test.com/v1/acct', 'token', 'container')[1]
        self.assertEqual(value, [])
        self.assertRequests([('GET', '/v1/acct/container?format=json', '', {'accept-encoding': 'gzip', 'x-auth-token': 'token'})])

    def test_param_marker(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&marker=marker')
        c.get_container('http://www.test.com/v1/acct', 'token', 'container', marker='marker')
        self.assertRequests([('GET', '/v1/acct/container?format=json&marker=marker', '', {'accept-encoding': 'gzip', 'x-auth-token': 'token'})])

    def test_param_limit(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&limit=10')
        c.get_container('http://www.test.com/v1/acct', 'token', 'container', limit=10)
        self.assertRequests([('GET', '/v1/acct/container?format=json&limit=10', '', {'accept-encoding': 'gzip', 'x-auth-token': 'token'})])

    def test_param_prefix(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&prefix=asdf/')
        c.get_container('http://www.test.com/v1/acct', 'token', 'container', prefix='asdf/')
        self.assertRequests([('GET', '/v1/acct/container?format=json&prefix=asdf/', '', {'accept-encoding': 'gzip', 'x-auth-token': 'token'})])

    def test_param_delimiter(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&delimiter=/')
        c.get_container('http://www.test.com/v1/acct', 'token', 'container', delimiter='/')
        self.assertRequests([('GET', '/v1/acct/container?format=json&delimiter=/', '', {'accept-encoding': 'gzip', 'x-auth-token': 'token'})])

    def test_param_end_marker(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&end_marker=end_marker')
        c.get_container('http://www.test.com/v1/acct', 'token', 'container', end_marker='end_marker')
        self.assertRequests([('GET', '/v1/acct/container?format=json&end_marker=end_marker', '', {'x-auth-token': 'token', 'accept-encoding': 'gzip'})])

    def test_param_path(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json&path=asdf')
        c.get_container('http://www.test.com/v1/acct', 'token', 'container', path='asdf')
        self.assertRequests([('GET', '/v1/acct/container?format=json&path=asdf', '', {'accept-encoding': 'gzip', 'x-auth-token': 'token'})])

    def test_request_headers(self):
        c.http_connection = self.fake_http_connection(204, query_string='format=json')
        conn = c.http_connection('http://www.test.com')
        headers = {'x-client-key': 'client key'}
        c.get_container('url_is_irrelevant', 'TOKEN', 'container', http_conn=conn, headers=headers)
        self.assertRequests([('GET', '/container?format=json', '', {'x-auth-token': 'TOKEN', 'x-client-key': 'client key', 'accept-encoding': 'gzip'})])

    def test_query_string(self):
        c.http_connection = self.fake_http_connection(200, query_string='format=json&hello=20', body=b'[]')
        c.get_container('http://www.test.com', 'asdf', 'asdf', query_string='hello=20')
        self.assertRequests([('GET', '/asdf?format=json&hello=20', '', {'accept-encoding': 'gzip', 'x-auth-token': 'asdf'})])

class TestHeadContainer(MockHttpTest):

    def test_head_ok(self):
        fake_conn = self.fake_http_connection(200, headers={'x-container-meta-color': 'blue'})
        with mock.patch('swiftclient.client.http_connection', new=fake_conn):
            resp = c.head_container('https://example.com/v1/AUTH_test', 'token', 'container')
        self.assertEqual(resp['x-container-meta-color'], 'blue')
        self.assertRequests([('HEAD', 'https://example.com/v1/AUTH_test/container', '', {'x-auth-token': 'token'})])

    def test_server_error(self):
        body = 'c' * 60
        headers = {'foo': 'bar'}
        c.http_connection = self.fake_http_connection(StubResponse(500, body, headers))
        with self.assertRaises(c.ClientException) as exc_context:
            c.head_container('http://www.test.com', 'asdf', 'container')
        e = exc_context.exception
        self.assertRequests([('HEAD', '/container', '', {'x-auth-token': 'asdf'})])
        self.assertEqual(e.http_status, 500)
        self.assertEqual(e.http_response_content, body)
        self.assertEqual(e.http_response_headers, headers)

class TestPutContainer(MockHttpTest):

    def test_ok(self):
        c.http_connection = self.fake_http_connection(200)
        value = c.put_container('http://www.test.com', 'token', 'container')
        self.assertIsNone(value)
        self.assertRequests([('PUT', '/container', '', {'x-auth-token': 'token', 'content-length': '0'})])

    def test_server_error(self):
        body = 'c' * 60
        headers = {'foo': 'bar'}
        c.http_connection = self.fake_http_connection(StubResponse(500, body, headers))
        with self.assertRaises(c.ClientException) as exc_context:
            c.put_container('http://www.test.com', 'token', 'container')
        self.assertEqual(exc_context.exception.http_response_content, body)
        self.assertEqual(exc_context.exception.http_response_headers, headers)
        self.assertRequests([('PUT', '/container', '', {'x-auth-token': 'token', 'content-length': '0'})])

    def test_query_string(self):
        c.http_connection = self.fake_http_connection(200, query_string='hello=20')
        c.put_container('http://www.test.com', 'asdf', 'asdf', query_string='hello=20')
        for req in self.iter_request_log():
            self.assertEqual(req['method'], 'PUT')
            self.assertEqual(req['parsed_path'].path, '/asdf')
            self.assertEqual(req['parsed_path'].query, 'hello=20')
            self.assertEqual(req['headers']['x-auth-token'], 'asdf')

class TestDeleteContainer(MockHttpTest):

    def test_ok(self):
        c.http_connection = self.fake_http_connection(200)
        value = c.delete_container('http://www.test.com', 'token', 'container')
        self.assertIsNone(value)
        self.assertRequests([('DELETE', '/container', '', {'x-auth-token': 'token'})])

    def test_query_string(self):
        c.http_connection = self.fake_http_connection(200, query_string='hello=20')
        c.delete_container('http://www.test.com', 'token', 'container', query_string='hello=20')
        self.assertRequests([('DELETE', 'http://www.test.com/container?hello=20', '', {'x-auth-token': 'token'})])

class TestGetObject(MockHttpTest):

    def test_server_error(self):
        body = 'c' * 60
        headers = {'foo': 'bar'}
        c.http_connection = self.fake_http_connection(StubResponse(500, body, headers))
        with self.assertRaises(c.ClientException) as exc_context:
            c.get_object('http://www.test.com', 'asdf', 'asdf', 'asdf')
        self.assertEqual(exc_context.exception.http_response_content, body)
        self.assertEqual(exc_context.exception.http_response_headers, headers)

    def test_query_string(self):
        c.http_connection = self.fake_http_connection(200, query_string='hello=20')
        c.get_object('http://www.test.com', 'asdf', 'asdf', 'asdf', query_string='hello=20')
        self.assertRequests([('GET', '/asdf/asdf?hello=20', '', {'x-auth-token': 'asdf'})])

    def test_get_object_as_string(self):
        c.http_connection = self.fake_http_connection(200, body='abcde')
        __, resp = c.get_object('http://storage.example.com', 'TOKEN', 'container_name', 'object_name')
        self.assertEqual(resp, 'abcde')

    def test_request_headers(self):
        c.http_connection = self.fake_http_connection(200)
        conn = c.http_connection('http://www.test.com')
        headers = {'Range': 'bytes=1-2'}
        c.get_object('url_is_irrelevant', 'TOKEN', 'container', 'object', http_conn=conn, headers=headers)
        self.assertRequests([('GET', '/container/object', '', {'x-auth-token': 'TOKEN', 'range': 'bytes=1-2'})])

    def test_response_headers(self):
        c.http_connection = self.fake_http_connection(200, headers={'X-Utf-8-Header': b't%c3%a9st', 'X-Non-Utf-8-Header': b'%ff', 'X-Binary-Header': b'\xff'})
        conn = c.http_connection('http://www.test.com')
        headers, data = c.get_object('url_is_irrelevant', 'TOKEN', 'container', 'object', http_conn=conn)
        self.assertEqual('tést', headers.get('x-utf-8-header', ''))
        self.assertEqual('%ff', headers.get('x-non-utf-8-header', ''))
        self.assertEqual('%FF', headers.get('x-binary-header', ''))

    def test_chunk_size_read_method(self):
        conn = c.Connection('http://auth.url/', 'some_user', 'some_key')
        with mock.patch('swiftclient.client.get_auth_1_0') as mock_get_auth:
            mock_get_auth.return_value = ('http://auth.url/', 'tToken')
            c.http_connection = self.fake_http_connection(200, body='abcde')
            __, resp = conn.get_object('asdf', 'asdf', resp_chunk_size=3)
            self.assertTrue(hasattr(resp, 'read'))
            self.assertEqual(resp.read(3), 'abc')
            self.assertEqual(resp.read(None), 'de')
            self.assertEqual(resp.read(), '')

    def test_chunk_size_iter(self):
        conn = c.Connection('http://auth.url/', 'some_user', 'some_key')
        with mock.patch('swiftclient.client.get_auth_1_0') as mock_get_auth:
            mock_get_auth.return_value = ('http://auth.url/', 'tToken')
            c.http_connection = self.fake_http_connection(200, body='abcde')
            __, resp = conn.get_object('asdf', 'asdf', resp_chunk_size=3)
            self.assertTrue(hasattr(resp, 'next'))
            self.assertEqual(next(resp), 'abc')
            self.assertEqual(next(resp), 'de')
            self.assertRaises(StopIteration, next, resp)

    def test_chunk_size_read_and_iter(self):
        conn = c.Connection('http://auth.url/', 'some_user', 'some_key')
        with mock.patch('swiftclient.client.get_auth_1_0') as mock_get_auth:
            mock_get_auth.return_value = ('http://auth.url/', 'tToken')
            c.http_connection = self.fake_http_connection(200, body='abcdef')
            __, resp = conn.get_object('asdf', 'asdf', resp_chunk_size=2)
            self.assertTrue(hasattr(resp, 'read'))
            self.assertEqual(resp.read(3), 'abc')
            self.assertEqual(next(resp), 'de')
            self.assertEqual(resp.read(), 'f')
            self.assertRaises(StopIteration, next, resp)
            self.assertEqual(resp.read(), '')

    def test_chunk_size_iter_chunked_no_retry(self):
        conn = c.Connection('http://auth.url/', 'some_user', 'some_key')
        with mock.patch('swiftclient.client.get_auth_1_0') as mock_get_auth:
            mock_get_auth.return_value = ('http://auth.url/', 'tToken')
            c.http_connection = self.fake_http_connection(200, body='abcdef', headers={'Transfer-Encoding': 'chunked'})
            __, resp = conn.get_object('asdf', 'asdf', resp_chunk_size=2)
            self.assertEqual(next(resp), 'ab')
            resp.resp.read()
            self.assertRaises(StopIteration, next, resp)

    def test_chunk_size_iter_retry(self):
        conn = c.Connection('http://auth.url/', 'some_user', 'some_key')
        with mock.patch('swiftclient.client.get_auth_1_0') as mock_get_auth:
            mock_get_auth.return_value = ('http://auth.url', 'tToken')
            c.http_connection = self.fake_http_connection(StubResponse(200, 'abcdef', {'etag': 'some etag', 'content-length': '6'}), StubResponse(206, 'cdef', {'etag': 'some etag', 'content-length': '4', 'content-range': 'bytes 2-5/6'}), StubResponse(206, 'ef', {'etag': 'some etag', 'content-length': '2', 'content-range': 'bytes 4-5/6'}))
            __, resp = conn.get_object('asdf', 'asdf', resp_chunk_size=2)
            self.assertEqual(next(resp), 'ab')
            self.assertEqual(1, conn.attempts)
            resp.resp.read()
            self.assertEqual(next(resp), 'cd')
            self.assertEqual(2, conn.attempts)
            resp.resp.read()
            self.assertEqual(next(resp), 'ef')
            self.assertEqual(3, conn.attempts)
            self.assertRaises(StopIteration, next, resp)
        self.assertRequests([('GET', '/asdf/asdf', '', {'x-auth-token': 'tToken'}), ('GET', '/asdf/asdf', '', {'range': 'bytes=2-', 'if-match': 'some etag', 'x-auth-token': 'tToken'}), ('GET', '/asdf/asdf', '', {'range': 'bytes=4-', 'if-match': 'some etag', 'x-auth-token': 'tToken'})])

    def test_chunk_size_iter_retry_no_range_support(self):
        conn = c.Connection('http://auth.url/', 'some_user', 'some_key')
        with mock.patch('swiftclient.client.get_auth_1_0') as mock_get_auth:
            mock_get_auth.return_value = ('http://auth.url', 'tToken')
            c.http_connection = self.fake_http_connection(*[StubResponse(200, 'abcdef', {'etag': 'some etag', 'content-length': '6'})] * 3)
            __, resp = conn.get_object('asdf', 'asdf', resp_chunk_size=2)
            self.assertEqual(next(resp), 'ab')
            self.assertEqual(1, conn.attempts)
            resp.resp.read()
            self.assertEqual(next(resp), 'cd')
            self.assertEqual(2, conn.attempts)
            resp.resp.read()
            self.assertEqual(next(resp), 'ef')
            self.assertEqual(3, conn.attempts)
            self.assertRaises(StopIteration, next, resp)
        self.assertRequests([('GET', '/asdf/asdf', '', {'x-auth-token': 'tToken'}), ('GET', '/asdf/asdf', '', {'range': 'bytes=2-', 'if-match': 'some etag', 'x-auth-token': 'tToken'}), ('GET', '/asdf/asdf', '', {'range': 'bytes=4-', 'if-match': 'some etag', 'x-auth-token': 'tToken'})])

    def test_chunk_size_iter_retry_bad_range_response(self):
        conn = c.Connection('http://auth.url/', 'some_user', 'some_key')
        with mock.patch('swiftclient.client.get_auth_1_0') as mock_get_auth:
            mock_get_auth.return_value = ('http://auth.url', 'tToken')
            c.http_connection = self.fake_http_connection(StubResponse(200, 'abcdef', {'etag': 'some etag', 'content-length': '6'}), StubResponse(206, 'abcdef', {'etag': 'some etag', 'content-length': '6', 'content-range': 'chunk 1-2/3'}))
            __, resp = conn.get_object('asdf', 'asdf', resp_chunk_size=2)
            self.assertEqual(next(resp), 'ab')
            self.assertEqual(1, conn.attempts)
            resp.resp.read()
            self.assertRaises(c.ClientException, next, resp)
        self.assertRequests([('GET', '/asdf/asdf', '', {'x-auth-token': 'tToken'}), ('GET', '/asdf/asdf', '', {'range': 'bytes=2-', 'if-match': 'some etag', 'x-auth-token': 'tToken'})])

    def test_get_object_with_resp_chunk_size_zero(self):

        def get_connection(self):

            def get_auth():
                return ('http://auth.test.com', 'token')
            conn = c.Connection('http://www.test.com', 'asdf', 'asdf')
            self.assertIs(type(conn), c.Connection)
            conn.get_auth = get_auth
            self.assertEqual(conn.attempts, 0)
            return conn
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
            conn = get_connection(self)
            conn.get_object('container1', 'obj1', resp_chunk_size=0)
            self.assertEqual(conn.attempts, 1)

class TestHeadObject(MockHttpTest):

    def test_server_error(self):
        body = 'c' * 60
        headers = {'foo': 'bar'}
        c.http_connection = self.fake_http_connection(StubResponse(500, body, headers))
        with self.assertRaises(c.ClientException) as exc_context:
            c.head_object('http://www.test.com', 'asdf', 'asdf', 'asdf')
        self.assertEqual(exc_context.exception.http_response_content, body)
        self.assertEqual(exc_context.exception.http_response_headers, headers)

    def test_request_headers(self):
        c.http_connection = self.fake_http_connection(204)
        conn = c.http_connection('http://www.test.com')
        headers = {'x-client-key': 'client key'}
        c.head_object('url_is_irrelevant', 'TOKEN', 'container', 'asdf', http_conn=conn, headers=headers)
        self.assertRequests([('HEAD', '/container/asdf', '', {'x-auth-token': 'TOKEN', 'x-client-key': 'client key'})])

    def test_query_string(self):
        c.http_connection = self.fake_http_connection(204)
        conn = c.http_connection('http://www.test.com')
        query_string = 'foo=bar'
        c.head_object('url_is_irrelevant', 'token', 'container', 'key', http_conn=conn, query_string=query_string)
        self.assertRequests([('HEAD', '/container/key?foo=bar', '', {'x-auth-token': 'token'})])

class TestPutObject(MockHttpTest):

    def test_ok(self):
        c.http_connection = self.fake_http_connection(200)
        args = ('http://www.test.com', 'TOKEN', 'container', 'obj', 'body', 4)
        value = c.put_object(*args)
        self.assertIsInstance(value, str)
        self.assertEqual(value, EMPTY_ETAG)
        self.assertRequests([('PUT', '/container/obj', 'body', {'x-auth-token': 'TOKEN', 'content-length': '4'})])

    def test_unicode_ok(self):
        conn = c.http_connection('http://www.test.com/')
        mock_file = io.StringIO('天空中的乌云')
        args = ('天空中的乌云', '天空中的乌云', '天空中的乌云', '天空中的乌云', mock_file)
        text = '天空中的乌云'
        headers = {'X-Header1': text, 'X-2': '1', 'X-3': "{'a': 'b'}", 'a-b': '.x:yz mn:fg:lp'}
        resp = MockHttpResponse()
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        value = c.put_object(*args, headers=headers, http_conn=conn)
        self.assertIsInstance(value, str)
        self.assertIn(('a-b', b'.x:yz mn:fg:lp'), resp.buffer)
        self.assertIn(('x-header1', text.encode('utf8')), resp.buffer)

    def test_chunk_warning(self):
        conn = c.http_connection('http://www.test.com/')
        mock_file = io.StringIO('asdf')
        args = ('asdf', 'asdf', 'asdf', 'asdf', mock_file)
        resp = MockHttpResponse()
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        with warnings.catch_warnings(record=True) as w:
            c.put_object(*args, chunk_size=20, headers={}, http_conn=conn)
            self.assertEqual(len(w), 0)
        body = 'c' * 60
        c.http_connection = self.fake_http_connection(200, body=body)
        args = ('http://www.test.com', 'asdf', 'asdf', 'asdf', 'asdf')
        with warnings.catch_warnings(record=True) as w:
            c.put_object(*args, chunk_size=20)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

    def test_server_error(self):
        body = 'c' * 60
        headers = {'foo': 'bar'}
        c.http_connection = self.fake_http_connection(StubResponse(500, body, headers))
        args = ('http://www.test.com', 'asdf', 'asdf', 'asdf', 'asdf')
        with self.assertRaises(c.ClientException) as exc_context:
            c.put_object(*args)
        e = exc_context.exception
        self.assertEqual(e.http_response_content, body)
        self.assertEqual(e.http_response_headers, headers)
        self.assertEqual(e.http_status, 500)
        self.assertRequests([('PUT', '/asdf/asdf', 'asdf', {'x-auth-token': 'asdf'})])

    def test_query_string(self):
        c.http_connection = self.fake_http_connection(200, query_string='hello=20')
        c.put_object('http://www.test.com', 'asdf', 'asdf', 'asdf', query_string='hello=20')
        for req in self.iter_request_log():
            self.assertEqual(req['method'], 'PUT')
            self.assertEqual(req['parsed_path'].path, '/asdf/asdf')
            self.assertEqual(req['parsed_path'].query, 'hello=20')
            self.assertEqual(req['headers']['x-auth-token'], 'asdf')

    def test_raw_upload(self):
        conn = c.http_connection('http://www.test.com/')
        resp = MockHttpResponse(status=200)
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        raw_data = b'asdf' * 256
        raw_data_len = len(raw_data)
        for kwarg in ({'headers': {'Content-Length': str(raw_data_len)}}, {'content_length': raw_data_len}):
            with tempfile.TemporaryFile() as mock_file:
                mock_file.write(raw_data)
                mock_file.seek(0)
                c.put_object(url='http://www.test.com', http_conn=conn, contents=mock_file, **kwarg)
                req_data = resp.requests_params['data']
                self.assertIs(type(req_data), swiftclient.utils.LengthWrapper)
                self.assertEqual(raw_data_len, len(req_data.read()))

    def test_chunk_upload(self):
        conn = c.http_connection('http://www.test.com/')
        resp = MockHttpResponse(status=200)
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        raw_data = b'asdf' * 256
        chunk_size = 16
        with tempfile.TemporaryFile() as mock_file:
            mock_file.write(raw_data)
            mock_file.seek(0)
            c.put_object(url='http://www.test.com', http_conn=conn, contents=mock_file, chunk_size=chunk_size)
            req_data = resp.requests_params['data']
            self.assertTrue(hasattr(req_data, '__iter__'))
            data = b''
            for chunk in req_data:
                self.assertEqual(chunk_size, len(chunk))
                data += chunk
            self.assertEqual(data, raw_data)

    def test_iter_upload(self):

        def data():
            for chunk in ('foo', '', 'bar'):
                yield chunk
        conn = c.http_connection('http://www.test.com/')
        resp = MockHttpResponse(status=200)
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        c.put_object(url='http://www.test.com', http_conn=conn, contents=data())
        req_headers = resp.requests_params['headers']
        self.assertNotIn('Content-Length', req_headers)
        req_data = resp.requests_params['data']
        self.assertTrue(hasattr(req_data, '__iter__'))
        self.assertEqual(['foo', 'bar'], list(req_data))

    def test_md5_mismatch(self):
        conn = c.http_connection('http://www.test.com')
        resp = MockHttpResponse(status=200, verify=True, headers={'etag': '"badresponseetag"'})
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        raw_data = b'asdf' * 256
        raw_data_md5 = md5(raw_data).hexdigest()
        chunk_size = 16
        with tempfile.TemporaryFile() as mock_file:
            mock_file.write(raw_data)
            mock_file.seek(0)
            contents = swiftclient.utils.ReadableToIterable(mock_file, md5=True)
            etag = c.put_object(url='http://www.test.com', http_conn=conn, contents=contents, chunk_size=chunk_size)
            self.assertNotEqual(etag, contents.get_md5sum())
            self.assertEqual(etag, 'badresponseetag')
            self.assertEqual(raw_data_md5, contents.get_md5sum())

    def test_md5_match(self):
        conn = c.http_connection('http://www.test.com')
        raw_data = b'asdf' * 256
        raw_data_md5 = md5(raw_data).hexdigest()
        resp = MockHttpResponse(status=200, verify=True, headers={'etag': '"' + raw_data_md5 + '"'})
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        chunk_size = 16
        with tempfile.TemporaryFile() as mock_file:
            mock_file.write(raw_data)
            mock_file.seek(0)
            contents = swiftclient.utils.ReadableToIterable(mock_file, md5=True)
            etag = c.put_object(url='http://www.test.com', http_conn=conn, contents=contents, chunk_size=chunk_size)
            self.assertEqual(raw_data_md5, contents.get_md5sum())
            self.assertEqual(etag, contents.get_md5sum())

    def test_params(self):
        conn = c.http_connection('http://www.test.com/')
        resp = MockHttpResponse(status=200)
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        c.put_object(url='http://www.test.com', http_conn=conn, etag='1234-5678', content_type='text/plain')
        request_header = resp.requests_params['headers']
        self.assertEqual(request_header['etag'], b'1234-5678')
        self.assertEqual(request_header['content-type'], b'text/plain')

    def test_no_content_type(self):
        conn = c.http_connection('http://www.test.com/')
        resp = MockHttpResponse(status=200)
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        c.put_object(url='http://www.test.com', http_conn=conn)
        request_header = resp.requests_params['headers']
        self.assertNotIn('content-type', request_header)

    def test_content_type_in_headers(self):
        conn = c.http_connection('http://www.test.com/')
        resp = MockHttpResponse(status=200)
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        hdrs = {'Content-Type': 'text/Plain'}
        c.put_object(url='http://www.test.com', http_conn=conn, headers=hdrs)
        request_header = resp.requests_params['headers']
        self.assertEqual(request_header['content-type'], b'text/Plain')
        c.put_object(url='http://www.test.com', http_conn=conn, headers=hdrs, content_type='image/jpeg')
        request_header = resp.requests_params['headers']
        self.assertEqual(request_header['content-type'], b'image/jpeg')

class TestPostObject(MockHttpTest):

    def test_ok(self):
        c.http_connection = self.fake_http_connection(200)
        delete_at = 2.1
        args = ('http://www.test.com', 'token', 'container', 'obj', {'X-Object-Meta-Test': 'mymeta', 'X-Delete-At': delete_at})
        c.post_object(*args)
        self.assertRequests([('POST', '/container/obj', '', {'x-auth-token': 'token', 'X-Object-Meta-Test': 'mymeta', 'X-Delete-At': delete_at})])
        self.assertEqual(args[-1], {'X-Object-Meta-Test': 'mymeta', 'X-Delete-At': delete_at})

    def test_unicode_ok(self):
        conn = c.http_connection('http://www.test.com/')
        args = ('天空中的乌云', '天空中的乌云', '天空中的乌云', '天空中的乌云')
        text = '天空中的乌云'
        headers = {'X-Header1': text, b'X-Header2': 'value', 'X-2': '1', 'X-3': "{'a': 'b'}", 'a-b': '.x:yz mn:kl:qr', 'X-Object-Meta-Header-not-encoded': text, b'X-Object-Meta-Header-encoded': 'value'}
        resp = MockHttpResponse()
        conn[1].getresponse = resp.fake_response
        conn[1]._request = resp._fake_request
        c.post_object(*args, headers=headers, http_conn=conn)
        self.assertIn(('a-b', b'.x:yz mn:kl:qr'), resp.buffer)
        self.assertIn(('x-header1', text.encode('utf8')), resp.buffer)
        self.assertIn((b'x-object-meta-header-not-encoded', text.encode('utf8')), resp.buffer)
        self.assertIn((b'x-object-meta-header-encoded', b'value'), resp.buffer)
        self.assertIn((b'x-header2', b'value'), resp.buffer)

    def test_server_error(self):
        body = 'c' * 60
        headers = {'foo': 'bar'}
        c.http_connection = self.fake_http_connection(StubResponse(500, body, headers))
        args = ('http://www.test.com', 'token', 'container', 'obj', {})
        with self.assertRaises(c.ClientException) as exc_context:
            c.post_object(*args)
        self.assertEqual(exc_context.exception.http_response_content, body)
        self.assertEqual(exc_context.exception.http_response_headers, headers)
        self.assertRequests([('POST', 'http://www.test.com/container/obj', '', {'x-auth-token': 'token'})])

class TestCopyObject(MockHttpTest):

    def test_server_error(self):
        c.http_connection = self.fake_http_connection(500)
        self.assertRaises(c.ClientException, c.copy_object, 'http://www.test.com/v1/AUTH', 'asdf', 'asdf', 'asdf')

    def test_ok(self):
        c.http_connection = self.fake_http_connection(200)
        c.copy_object('http://www.test.com/v1/AUTH', 'token', 'container', 'obj', destination='/container2/obj')
        self.assertRequests([('COPY', 'http://www.test.com/v1/AUTH/container/obj', '', {'X-Auth-Token': 'token', 'Destination': '/container2/obj'})])

    def test_service_token(self):
        c.http_connection = self.fake_http_connection(200)
        c.copy_object('http://www.test.com/v1/AUTH', None, 'container', 'obj', destination='/container2/obj', service_token='TOKEN')
        self.assertRequests([('COPY', 'http://www.test.com/v1/AUTH/container/obj', '', {'X-Service-Token': 'TOKEN', 'Destination': '/container2/obj'})])

    def test_headers(self):
        c.http_connection = self.fake_http_connection(200)
        c.copy_object('http://www.test.com/v1/AUTH', 'token', 'container', 'obj', destination='/container2/obj', headers={'some-hdr': 'a', 'other-hdr': 'b'})
        self.assertRequests([('COPY', 'http://www.test.com/v1/AUTH/container/obj', '', {'X-Auth-Token': 'token', 'Destination': '/container2/obj', 'some-hdr': 'a', 'other-hdr': 'b'})])

    def test_fresh_metadata_default(self):
        c.http_connection = self.fake_http_connection(200)
        c.copy_object('http://www.test.com/v1/AUTH', 'token', 'container', 'obj', '/container2/obj', {'x-fresh-metadata': 'hdr-value'})
        self.assertRequests([('COPY', 'http://www.test.com/v1/AUTH/container/obj', '', {'X-Auth-Token': 'token', 'Destination': '/container2/obj', 'X-Fresh-Metadata': 'hdr-value'})])

    def test_fresh_metadata_true(self):
        c.http_connection = self.fake_http_connection(200)
        c.copy_object('http://www.test.com/v1/AUTH', 'token', 'container', 'obj', destination='/container2/obj', headers={'x-fresh-metadata': 'hdr-value'}, fresh_metadata=True)
        self.assertRequests([('COPY', 'http://www.test.com/v1/AUTH/container/obj', '', {'X-Auth-Token': 'token', 'Destination': '/container2/obj', 'X-Fresh-Metadata': 'true'})])

    def test_fresh_metadata_false(self):
        c.http_connection = self.fake_http_connection(200)
        c.copy_object('http://www.test.com/v1/AUTH', 'token', 'container', 'obj', destination='/container2/obj', headers={'x-fresh-metadata': 'hdr-value'}, fresh_metadata=False)
        self.assertRequests([('COPY', 'http://www.test.com/v1/AUTH/container/obj', '', {'x-auth-token': 'token', 'Destination': '/container2/obj', 'X-Fresh-Metadata': 'false'})])

    def test_no_destination(self):
        c.http_connection = self.fake_http_connection(200)
        c.copy_object('http://www.test.com/v1/AUTH', 'token', 'container', 'obj')
        self.assertRequests([('COPY', 'http://www.test.com/v1/AUTH/container/obj', '', {'x-auth-token': 'token', 'Destination': '/container/obj'})])

class TestDeleteObject(MockHttpTest):

    def test_ok(self):
        c.http_connection = self.fake_http_connection(200)
        c.delete_object('http://www.test.com', 'token', 'container', 'obj')
        self.assertRequests([('DELETE', 'http://www.test.com/container/obj', '', {'x-auth-token': 'token'})])

    def test_server_error(self):
        body = 'c' * 60
        headers = {'foo': 'bar'}
        c.http_connection = self.fake_http_connection(StubResponse(500, body, headers))
        with self.assertRaises(c.ClientException) as exc_context:
            c.delete_object('http://www.test.com', 'asdf', 'asdf', 'asdf')
        self.assertEqual(exc_context.exception.http_response_content, body)
        self.assertEqual(exc_context.exception.http_response_headers, headers)

    def test_query_string(self):
        c.http_connection = self.fake_http_connection(200, query_string='hello=20')
        c.delete_object('http://www.test.com', 'token', 'container', 'obj', query_string='hello=20')
        self.assertRequests([('DELETE', 'http://www.test.com/container/obj?hello=20', '', {'x-auth-token': 'token'})])

class TestGetCapabilities(MockHttpTest):

    def test_ok(self):
        conn = self.fake_http_connection(200, body=b'{}')
        http_conn = conn('http://www.test.com/info')
        info = c.get_capabilities(http_conn)
        self.assertRequests([('GET', '/info', '', {'Accept-Encoding': 'gzip'})])
        self.assertEqual(info, {})
        self.assertTrue(http_conn[1].resp.has_been_read)

    def test_server_error(self):
        body = 'c' * 60
        headers = {'foo': 'bar'}
        conn = self.fake_http_connection(StubResponse(500, body, headers))
        http_conn = conn('http://www.test.com/info')
        with self.assertRaises(c.ClientException) as exc_context:
            c.get_capabilities(http_conn)
        self.assertEqual(exc_context.exception.http_response_content, body)
        self.assertEqual(exc_context.exception.http_response_headers, headers)

    def test_conn_get_capabilities_with_auth(self):
        auth_headers = {'x-auth-token': 'token', 'x-storage-url': 'http://storage.example.com/v1/AUTH_test'}
        auth_v1_response = StubResponse(headers=auth_headers)
        stub_info = {'swift': {'fake': True}}
        info_response = StubResponse(body=b'{"swift":{"fake":true}}')
        fake_conn = self.fake_http_connection(auth_v1_response, info_response)
        conn = c.Connection('http://auth.example.com/auth/v1.0', 'user', 'key')
        with mock.patch('swiftclient.client.http_connection', new=fake_conn):
            info = conn.get_capabilities()
        self.assertEqual(info, stub_info)
        self.assertRequests([('GET', '/auth/v1.0', '', {'x-auth-user': 'user', 'x-auth-key': 'key'}), ('GET', 'http://storage.example.com/info', '', {'accept-encoding': 'gzip'})])

    def test_conn_get_capabilities_with_os_auth(self):
        fake_keystone = fake_get_auth_keystone(storage_url='http://storage.example.com/v1/AUTH_test')
        stub_info = {'swift': {'fake': True}}
        info_response = StubResponse(body=b'{"swift":{"fake":true}}')
        fake_conn = self.fake_http_connection(info_response)
        os_options = {'project_id': 'test'}
        conn = c.Connection('http://keystone.example.com/v3.0', 'user', 'key', os_options=os_options, auth_version=3)
        with mock.patch.multiple('swiftclient.client', get_auth_keystone=fake_keystone, http_connection=fake_conn):
            info = conn.get_capabilities()
        self.assertEqual(info, stub_info)
        self.assertRequests([('GET', 'http://storage.example.com/info')])

    def test_conn_get_capabilities_with_url_param(self):
        stub_info = {'swift': {'fake': True}}
        info_response = StubResponse(body=b'{"swift":{"fake":true}}')
        fake_conn = self.fake_http_connection(info_response)
        conn = c.Connection('http://auth.example.com/auth/v1.0', 'user', 'key')
        with mock.patch('swiftclient.client.http_connection', new=fake_conn):
            info = conn.get_capabilities('http://other-storage.example.com/info')
        self.assertEqual(info, stub_info)
        self.assertRequests([('GET', 'http://other-storage.example.com/info')])

    def test_conn_get_capabilities_with_preauthurl_param(self):
        stub_info = {'swift': {'fake': True}}
        info_response = StubResponse(body=b'{"swift":{"fake":true}}')
        fake_conn = self.fake_http_connection(info_response)
        storage_url = 'http://storage.example.com/v1/AUTH_test'
        conn = c.Connection('http://auth.example.com/auth/v1.0', 'user', 'key', preauthurl=storage_url)
        with mock.patch('swiftclient.client.http_connection', new=fake_conn):
            info = conn.get_capabilities()
        self.assertEqual(info, stub_info)
        self.assertRequests([('GET', 'http://storage.example.com/info')])

    def test_conn_get_capabilities_with_os_options(self):
        stub_info = {'swift': {'fake': True}}
        info_response = StubResponse(body=b'{"swift":{"fake":true}}')
        fake_conn = self.fake_http_connection(info_response)
        storage_url = 'http://storage.example.com/v1/AUTH_test'
        os_options = {'project_id': 'test', 'object_storage_url': storage_url}
        conn = c.Connection('http://keystone.example.com/v3.0', 'user', 'key', os_options=os_options, auth_version=3)
        with mock.patch('swiftclient.client.http_connection', new=fake_conn):
            info = conn.get_capabilities()
        self.assertEqual(info, stub_info)
        self.assertRequests([('GET', 'http://storage.example.com/info')])

class TestHTTPConnection(MockHttpTest):

    def test_bad_url_scheme(self):
        url = 'www.test.com'
        with self.assertRaises(c.ClientException) as exc_context:
            c.http_connection(url)
        exc = exc_context.exception
        expected = 'Unsupported scheme "" in url "www.test.com"'
        self.assertEqual(expected, str(exc))
        url = '://www.test.com'
        with self.assertRaises(c.ClientException) as exc_context:
            c.http_connection(url)
        exc = exc_context.exception
        expected = 'Unsupported scheme "" in url "://www.test.com"'
        self.assertEqual(expected, str(exc))
        url = 'blah://www.test.com'
        with self.assertRaises(c.ClientException) as exc_context:
            c.http_connection(url)
        exc = exc_context.exception
        expected = 'Unsupported scheme "blah" in url "blah://www.test.com"'
        self.assertEqual(expected, str(exc))

    def test_ok_url_scheme(self):
        for scheme in ('http', 'https', 'HTTP', 'HTTPS'):
            url = '%s://www.test.com' % scheme
            parsed_url, conn = c.http_connection(url)
            self.assertEqual(scheme.lower(), parsed_url.scheme)
            self.assertEqual('%s://www.test.com' % scheme, conn.url)

    def test_ok_proxy(self):
        conn = c.http_connection('http://www.test.com/', proxy='http://localhost:8080')
        self.assertEqual(conn[1].requests_args['proxies']['http'], 'http://localhost:8080')

    def test_bad_proxy(self):
        try:
            c.http_connection('http://www.test.com/', proxy='localhost:8080')
        except c.ClientException as e:
            self.assertEqual(e.msg, "Proxy's missing scheme")

    def test_cacert(self):
        conn = c.http_connection('http://www.test.com/', cacert='/dev/urandom')
        self.assertEqual(conn[1].requests_args['verify'], '/dev/urandom')

    def test_insecure(self):
        conn = c.http_connection('http://www.test.com/', insecure=True)
        self.assertEqual(conn[1].requests_args['verify'], False)

    def test_cert(self):
        conn = c.http_connection('http://www.test.com/', cert='minnie')
        self.assertEqual(conn[1].requests_args['cert'], 'minnie')

    def test_cert_key(self):
        conn = c.http_connection('http://www.test.com/', cert='minnie', cert_key='mickey')
        self.assertEqual(conn[1].requests_args['cert'], ('minnie', 'mickey'))

    def test_response_connection_released(self):
        _parsed_url, conn = c.http_connection('http://www.test.com/')
        conn.resp = MockHttpResponse()
        conn.resp.raw = mock.Mock()
        conn.resp.raw.read.side_effect = ['Chunk', '']
        resp = conn.getresponse()
        self.assertFalse(resp.closed)
        self.assertEqual('Chunk', resp.read())
        self.assertFalse(resp.read())
        self.assertTrue(resp.closed)

    def test_response_headers(self):
        """Test latin1-encoded headers.
        """
        _, conn = c.http_connection('http://www.test.com/')
        conn.resp = MockHttpResponse(status=200, headers={b'\xd8\xaa-unicode'.decode('iso-8859-1'): b'\xd8\xaa-value'.decode('iso-8859-1'), 'empty-header': ''})
        resp = conn.getresponse()
        self.assertEqual('ت-value', resp.getheader('ت-unicode'))
        self.assertEqual('ت-value', resp.getheader('ت-UNICODE'))
        self.assertEqual('', resp.getheader('empty-header'))
        self.assertEqual(dict([('ت-unicode', 'ت-value'), ('empty-header', ''), ('etag', '"%s"' % EMPTY_ETAG)]), dict(resp.getheaders()))

class TestConnection(MockHttpTest):

    def test_instance(self):
        conn = c.Connection('http://www.test.com', 'asdf', 'asdf')
        self.assertEqual(conn.retries, 5)

    def test_instance_kwargs(self):
        args = {'user': 'ausername', 'key': 'secretpass', 'authurl': 'http://www.test.com', 'tenant_name': 'atenant'}
        conn = c.Connection(**args)
        self.assertEqual(type(conn), c.Connection)

    def test_instance_kwargs_token(self):
        args = {'preauthtoken': 'atoken123', 'preauthurl': 'http://www.test.com:8080/v1/AUTH_123456'}
        conn = c.Connection(**args)
        self.assertEqual(conn.url, args['preauthurl'])
        self.assertEqual(conn.token, args['preauthtoken'])

    def test_instance_kwargs_os_token(self):
        storage_url = 'http://storage.example.com/v1/AUTH_test'
        token = 'token'
        args = {'os_options': {'object_storage_url': storage_url, 'auth_token': token}}
        conn = c.Connection(**args)
        self.assertEqual(conn.url, storage_url)
        self.assertEqual(conn.token, token)

    def test_instance_kwargs_token_precedence(self):
        storage_url = 'http://storage.example.com/v1/AUTH_test'
        token = 'token'
        args = {'preauthurl': storage_url, 'preauthtoken': token, 'os_options': {'auth_token': 'less-specific-token', 'object_storage_url': 'less-specific-storage-url'}}
        conn = c.Connection(**args)
        self.assertEqual(conn.url, storage_url)
        self.assertEqual(conn.token, token)

    def test_storage_url_override(self):
        static_url = 'http://overridden.storage.url'
        conn = c.Connection('http://auth.url/', 'some_user', 'some_key', os_options={'object_storage_url': static_url})
        method_signatures = ((conn.head_account, []), (conn.get_account, []), (conn.head_container, ('asdf',)), (conn.get_container, ('asdf',)), (conn.put_container, ('asdf',)), (conn.delete_container, ('asdf',)), (conn.head_object, ('asdf', 'asdf')), (conn.get_object, ('asdf', 'asdf')), (conn.put_object, ('asdf', 'asdf', 'asdf')), (conn.post_object, ('asdf', 'asdf', {})), (conn.delete_object, ('asdf', 'asdf')))
        with mock.patch('swiftclient.client.get_auth_1_0') as mock_get_auth:
            mock_get_auth.return_value = ('http://auth.storage.url', 'tToken')
            for method, args in method_signatures:
                c.http_connection = self.fake_http_connection(200, body=b'[]', storage_url=static_url)
                method(*args)
                self.assertEqual(len(self.request_log), 1)
                for request in self.iter_request_log():
                    self.assertEqual(request['parsed_path'].netloc, 'overridden.storage.url')
                    self.assertEqual(request['headers']['x-auth-token'], 'tToken')

    def test_url_mapping(self):
        conn = c.Connection()
        uri_versions = {'http://storage.test.com': 'http://storage.test.com/info', 'http://storage.test.com/': 'http://storage.test.com/info', 'http://storage.test.com/v1': 'http://storage.test.com/info', 'http://storage.test.com/v1/': 'http://storage.test.com/info', 'http://storage.test.com/swift': 'http://storage.test.com/swift/info', 'http://storage.test.com/swift/': 'http://storage.test.com/swift/info', 'http://storage.test.com/v1.0': 'http://storage.test.com/info', 'http://storage.test.com/swift/v1.0': 'http://storage.test.com/swift/info', 'http://storage.test.com/v111': 'http://storage.test.com/info', 'http://storage.test.com/v111/test': 'http://storage.test.com/info', 'http://storage.test.com/v1/test': 'http://storage.test.com/info', 'http://storage.test.com/swift/v1.0/test': 'http://storage.test.com/swift/info', 'http://storage.test.com/v1.0/test': 'http://storage.test.com/info'}
        for uri_k, uri_v in uri_versions.items():
            self.assertEqual(conn._map_url(uri_k), uri_v)

    def test_get_capabilities(self):
        conn = c.Connection()
        with mock.patch('swiftclient.client.get_capabilities') as get_cap:
            conn.get_capabilities('http://storage2.test.com')
            parsed = get_cap.call_args[0][0][0]
            self.assertEqual(parsed.path, '/info')
            self.assertEqual(parsed.netloc, 'storage2.test.com')
            conn.get_auth = lambda: ('http://storage.test.com/v1/AUTH_test', 'token')
            conn.get_capabilities()
            parsed = get_cap.call_args[0][0][0]
            self.assertEqual(parsed.path, '/info')
            self.assertEqual(parsed.netloc, 'storage.test.com')

    def test_retry(self):

        def quick_sleep(*args):
            pass
        c.sleep = quick_sleep
        conn = c.Connection('http://www.test.com', 'asdf', 'asdf')
        code_iter = [500] * (conn.retries + 1)
        c.http_connection = self.fake_http_connection(*code_iter)
        self.assertRaises(c.ClientException, conn.head_account)
        self.assertEqual(conn.attempts, conn.retries + 1)

    def test_retry_on_ratelimit(self):

        def quick_sleep(*args):
            pass
        c.sleep = quick_sleep

        def test_status_code(code):
            conn = c.Connection('http://www.test.com/auth/v1.0', 'asdf', 'asdf', retry_on_ratelimit=True)
            code_iter = [200] + [code] * (conn.retries + 1)
            auth_resp_headers = {'x-auth-token': 'asdf', 'x-storage-url': 'http://storage/v1/test'}
            c.http_connection = self.fake_http_connection(*code_iter, headers=auth_resp_headers)
            with self.assertRaises(c.ClientException) as exc_context:
                conn.head_account()
            self.assertIn('Account HEAD failed', str(exc_context.exception))
            self.assertEqual(code, exc_context.exception.http_status)
            self.assertEqual(conn.attempts, conn.retries + 1)
            c.http_connection = self.fake_http_connection(200, code, headers=auth_resp_headers)
            conn = c.Connection('http://www.test.com/auth/v1.0', 'asdf', 'asdf', retry_on_ratelimit=False)
            with self.assertRaises(c.ClientException) as exc_context:
                conn.head_account()
            self.assertIn('Account HEAD failed', str(exc_context.exception))
            self.assertEqual(code, exc_context.exception.http_status)
            self.assertEqual(conn.attempts, 1)
        test_status_code(498)
        test_status_code(429)

    def test_retry_with_socket_error(self):

        def quick_sleep(*args):
            pass
        c.sleep = quick_sleep
        conn = c.Connection('http://www.test.com', 'asdf', 'asdf')
        with mock.patch('swiftclient.client.http_connection') as fake_http_connection, mock.patch('swiftclient.client.get_auth_1_0') as mock_auth:
            mock_auth.return_value = ('http://mock.com', 'mock_token')
            fake_http_connection.side_effect = socket.error
            self.assertRaises(socket.error, conn.head_account)
        self.assertEqual(mock_auth.call_count, 1)
        self.assertEqual(conn.attempts, conn.retries + 1)

    def test_retry_with_force_auth_retry_exceptions(self):

        def quick_sleep(*args):
            pass

        def do_test(exception):
            c.sleep = quick_sleep
            conn = c.Connection('http://www.test.com', 'asdf', 'asdf', force_auth_retry=True)
            with mock.patch('swiftclient.client.http_connection') as fake_http_connection, mock.patch('swiftclient.client.get_auth_1_0') as mock_auth:
                mock_auth.return_value = ('http://mock.com', 'mock_token')
                fake_http_connection.side_effect = exception
                self.assertRaises(exception, conn.head_account)
            self.assertEqual(mock_auth.call_count, conn.retries + 1)
            self.assertEqual(conn.attempts, conn.retries + 1)
        do_test(socket.error)
        do_test(RequestException)

    def test_retry_with_force_auth_retry_client_exceptions(self):

        def quick_sleep(*args):
            pass

        def do_test(http_status, count):

            def mock_http_connection(*args, **kwargs):
                raise ClientException('fake', http_status=http_status)
            c.sleep = quick_sleep
            conn = c.Connection('http://www.test.com', 'asdf', 'asdf', force_auth_retry=True)
            with mock.patch('swiftclient.client.http_connection') as fake_http_connection, mock.patch('swiftclient.client.get_auth_1_0') as mock_auth:
                mock_auth.return_value = ('http://mock.com', 'mock_token')
                fake_http_connection.side_effect = mock_http_connection
                self.assertRaises(ClientException, conn.head_account)
            self.assertEqual(mock_auth.call_count, count)
            self.assertEqual(conn.attempts, count)
        do_test(401, 2)
        do_test(408, 6)
        do_test(500, 6)
        do_test(503, 6)

    def test_resp_read_on_server_error(self):
        conn = c.Connection('http://www.test.com', 'asdf', 'asdf', retries=0)

        def get_auth(*args, **kwargs):
            return ('http://www.new.com', 'new')
        conn.get_auth = get_auth
        self.url, self.token = conn.get_auth()
        method_signatures = ((conn.head_account, []), (conn.get_account, []), (conn.head_container, ('asdf',)), (conn.get_container, ('asdf',)), (conn.put_container, ('asdf',)), (conn.delete_container, ('asdf',)), (conn.head_object, ('asdf', 'asdf')), (conn.get_object, ('asdf', 'asdf')), (conn.put_object, ('asdf', 'asdf', 'asdf')), (conn.post_object, ('asdf', 'asdf', {})), (conn.delete_object, ('asdf', 'asdf')))
        for method, args in method_signatures:
            c.http_connection = self.fake_http_connection(500)
            self.assertRaises(c.ClientException, method, *args)
            requests = list(self.iter_request_log())
            self.assertEqual(len(requests), 1)
            for req in requests:
                msg = '%s did not read resp on server error' % method.__name__
                self.assertTrue(req['resp'].has_been_read, msg)

    def test_reauth(self):
        c.http_connection = self.fake_http_connection(401, 200)

        def get_auth(*args, **kwargs):
            return ('http://www.new.com', 'new')

        def swap_sleep(*args):
            self.swap_sleep_called = True
            c.get_auth = get_auth
        c.sleep = swap_sleep
        self.swap_sleep_called = False
        conn = c.Connection('http://www.test.com', 'asdf', 'asdf', preauthurl='http://www.old.com', preauthtoken='old')
        self.assertEqual(conn.attempts, 0)
        self.assertEqual(conn.url, 'http://www.old.com')
        self.assertEqual(conn.token, 'old')
        conn.head_account()
        self.assertTrue(self.swap_sleep_called)
        self.assertEqual(conn.attempts, 2)
        self.assertEqual(conn.url, 'http://www.new.com')
        self.assertEqual(conn.token, 'new')

    def test_reauth_preauth(self):
        conn = c.Connection('http://auth.example.com', 'user', 'password', preauthurl='http://storage.example.com/v1/AUTH_test', preauthtoken='expired')
        auth_v1_response = StubResponse(200, headers={'x-auth-token': 'token', 'x-storage-url': 'http://storage.example.com/v1/AUTH_user'})
        fake_conn = self.fake_http_connection(401, auth_v1_response, 200)
        with mock.patch.multiple('swiftclient.client', http_connection=fake_conn, sleep=mock.DEFAULT):
            conn.head_account()
        self.assertRequests([('HEAD', '/v1/AUTH_test', '', {'x-auth-token': 'expired'}), ('GET', 'http://auth.example.com', '', {'x-auth-user': 'user', 'x-auth-key': 'password'}), ('HEAD', '/v1/AUTH_test', '', {'x-auth-token': 'token'})])

    def test_reauth_os_preauth(self):
        os_preauth_options = {'tenant_name': 'demo', 'object_storage_url': 'http://storage.example.com/v1/AUTH_test', 'auth_token': 'expired'}
        conn = c.Connection('http://auth.example.com', 'user', 'password', os_options=os_preauth_options, auth_version=2)
        fake_keystone = fake_get_auth_keystone(os_preauth_options)
        fake_conn = self.fake_http_connection(401, 200)
        with mock.patch.multiple('swiftclient.client', get_auth_keystone=fake_keystone, http_connection=fake_conn, sleep=mock.DEFAULT):
            conn.head_account()
        self.assertRequests([('HEAD', '/v1/AUTH_test', '', {'x-auth-token': 'expired'}), ('HEAD', '/v1/AUTH_test', '', {'x-auth-token': 'token'})])

    def test_session_no_invalidate(self):
        mock_session = mock.MagicMock()
        mock_session.get_endpoint.return_value = 'http://storagehost/v1/acct'
        mock_session.get_token.return_value = 'expired'
        mock_session.invalidate.return_value = False
        conn = c.Connection(session=mock_session)
        fake_conn = self.fake_http_connection(401)
        with mock.patch.multiple('swiftclient.client', http_connection=fake_conn, sleep=mock.DEFAULT):
            self.assertRaises(c.ClientException, conn.head_account)
        self.assertEqual(mock_session.get_token.mock_calls, [mock.call()])
        self.assertEqual(mock_session.invalidate.mock_calls, [mock.call()])

    def test_session_can_invalidate(self):
        mock_session = mock.MagicMock()
        mock_session.get_endpoint.return_value = 'http://storagehost/v1/acct'
        mock_session.get_token.side_effect = ['expired', 'token']
        mock_session.invalidate.return_value = True
        conn = c.Connection(session=mock_session)
        fake_conn = self.fake_http_connection(401, 200)
        with mock.patch.multiple('swiftclient.client', http_connection=fake_conn, sleep=mock.DEFAULT):
            conn.head_account()
        self.assertRequests([('HEAD', '/v1/acct', '', {'x-auth-token': 'expired'}), ('HEAD', '/v1/acct', '', {'x-auth-token': 'token'})])
        self.assertEqual(mock_session.get_token.mock_calls, [mock.call(), mock.call()])
        self.assertEqual(mock_session.invalidate.mock_calls, [mock.call()])

    def test_preauth_token_with_no_storage_url_requires_auth(self):
        conn = c.Connection('http://auth.example.com', 'user', 'password', preauthtoken='expired')
        auth_v1_response = StubResponse(200, headers={'x-auth-token': 'token', 'x-storage-url': 'http://storage.example.com/v1/AUTH_user'})
        fake_conn = self.fake_http_connection(auth_v1_response, 200)
        with mock.patch.multiple('swiftclient.client', http_connection=fake_conn, sleep=mock.DEFAULT):
            conn.head_account()
        self.assertRequests([('GET', 'http://auth.example.com', '', {'x-auth-user': 'user', 'x-auth-key': 'password'}), ('HEAD', '/v1/AUTH_user', '', {'x-auth-token': 'token'})])

    def test_os_preauth_token_with_no_storage_url_requires_auth(self):
        os_preauth_options = {'tenant_name': 'demo', 'auth_token': 'expired'}
        conn = c.Connection('http://auth.example.com', 'user', 'password', os_options=os_preauth_options, auth_version=2)
        storage_url = 'http://storage.example.com/v1/AUTH_user'
        fake_keystone = fake_get_auth_keystone(storage_url=storage_url)
        fake_conn = self.fake_http_connection(200)
        with mock.patch.multiple('swiftclient.client', get_auth_keystone=fake_keystone, http_connection=fake_conn, sleep=mock.DEFAULT):
            conn.head_account()
        self.assertRequests([('HEAD', '/v1/AUTH_user', '', {'x-auth-token': 'token'})])

    def test_preauth_url_trumps_auth_url(self):
        storage_url = 'http://storage.example.com/v1/AUTH_pre_url'
        conn = c.Connection('http://auth.example.com', 'user', 'password', preauthurl=storage_url)
        auth_v1_response = StubResponse(200, headers={'x-auth-token': 'post_token', 'x-storage-url': 'http://storage.example.com/v1/AUTH_post_url'})
        fake_conn = self.fake_http_connection(auth_v1_response, 200)
        with mock.patch.multiple('swiftclient.client', http_connection=fake_conn, sleep=mock.DEFAULT):
            conn.head_account()
        self.assertRequests([('GET', 'http://auth.example.com', '', {'x-auth-user': 'user', 'x-auth-key': 'password'}), ('HEAD', '/v1/AUTH_pre_url', '', {'x-auth-token': 'post_token'})])

    def test_os_preauth_url_trumps_auth_url(self):
        storage_url = 'http://storage.example.com/v1/AUTH_pre_url'
        os_preauth_options = {'tenant_name': 'demo', 'object_storage_url': storage_url}
        conn = c.Connection('http://auth.example.com', 'user', 'password', os_options=os_preauth_options, auth_version=2)
        fake_keystone = fake_get_auth_keystone(storage_url='http://storage.example.com/v1/AUTH_post_url', token='post_token')
        fake_conn = self.fake_http_connection(200)
        with mock.patch.multiple('swiftclient.client', get_auth_keystone=fake_keystone, http_connection=fake_conn, sleep=mock.DEFAULT):
            conn.head_account()
        self.assertRequests([('HEAD', '/v1/AUTH_pre_url', '', {'x-auth-token': 'post_token'})])

    def test_preauth_url_trumps_os_preauth_url(self):
        storage_url = 'http://storage.example.com/v1/AUTH_pre_url'
        os_storage_url = 'http://storage.example.com/v1/AUTH_os_pre_url'
        os_preauth_options = {'tenant_name': 'demo', 'object_storage_url': os_storage_url}
        orig_os_preauth_options = dict(os_preauth_options)
        conn = c.Connection('http://auth.example.com', 'user', 'password', os_options=os_preauth_options, auth_version=2, preauthurl=storage_url, tenant_name='not_demo')
        fake_keystone = fake_get_auth_keystone(storage_url='http://storage.example.com/v1/AUTH_post_url', token='post_token')
        fake_conn = self.fake_http_connection(200)
        with mock.patch.multiple('swiftclient.client', get_auth_keystone=fake_keystone, http_connection=fake_conn, sleep=mock.DEFAULT):
            conn.head_account()
        self.assertRequests([('HEAD', '/v1/AUTH_pre_url', '', {'x-auth-token': 'post_token'})])
        self.assertEqual(orig_os_preauth_options, os_preauth_options)

    def test_get_auth_sets_url_and_token(self):
        with mock.patch('swiftclient.client.get_auth') as mock_get_auth:
            mock_get_auth.return_value = ('https://storage.url/v1/AUTH_storage_acct', 'AUTH_token')
            conn = c.Connection('https://auth.url/auth/v2.0', 'user', 'passkey', tenant_name='tenant')
            conn.get_auth()
        self.assertEqual('https://storage.url/v1/AUTH_storage_acct', conn.url)
        self.assertEqual('AUTH_token', conn.token)

    def test_timeout_passed_down(self):
        orig_http_connection = c.http_connection
        timeouts = []

        def my_request_handler(*a, **kw):
            if 'timeout' in kw:
                timeouts.append(kw['timeout'])
            else:
                timeouts.append(None)
            return MockHttpResponse(status=200, headers={'x-auth-token': 'a_token', 'x-storage-url': 'http://files.example.com/v1/AUTH_user'})

        def shim_connection(*a, **kw):
            url, conn = orig_http_connection(*a, **kw)
            conn._request = my_request_handler
            return (url, conn)
        conn = c.Connection('http://auth.example.com', 'user', 'password', timeout=33.0)
        with mock.patch.multiple('swiftclient.client', http_connection=shim_connection, sleep=mock.DEFAULT):
            conn.head_account()
        self.assertEqual(timeouts, [33.0, 33.0])
        timeouts = []
        os_options = {'tenant_name': 'tenant', 'auth_token': 'meta-token'}
        conn = c.Connection('http://auth.example.com', 'user', 'password', timeout=33.0, os_options=os_options, auth_version=2.0)
        fake_ks = FakeKeystone(endpoint='http://some_url', token='secret')
        with mock.patch('swiftclient.client.ksclient_v2', fake_ks):
            with mock.patch.multiple('swiftclient.client', http_connection=shim_connection, sleep=mock.DEFAULT):
                conn.head_account()
        self.assertEqual(1, len(fake_ks.calls))
        self.assertEqual(33.0, fake_ks.calls[0].get('timeout'))
        self.assertEqual(timeouts, [33.0])
        self.assertIn('token', fake_ks.calls[0])
        self.assertEqual('meta-token', fake_ks.calls[0].get('token'))

    def test_reset_stream(self):

        class LocalContents:

            def __init__(self, tell_value=0):
                self.data = io.BytesIO(string.ascii_letters.encode() * 10)
                self.data.seek(tell_value)
                self.reads = []
                self.seeks = []
                self.tells = []

            def tell(self):
                self.tells.append(self.data.tell())
                return self.tells[-1]

            def seek(self, position, mode=0):
                self.seeks.append((position, mode))
                self.data.seek(position, mode)

            def read(self, size=-1):
                read_data = self.data.read(size)
                self.reads.append((size, read_data))
                return read_data

        class LocalConnection:

            def __init__(self, parsed_url=None):
                self.reason = ''
                if parsed_url:
                    self.host = parsed_url.netloc
                    self.port = parsed_url.netloc

            def putrequest(self, *args, **kwargs):
                self.send('PUT', *args, **kwargs)

            def putheader(self, *args, **kwargs):
                return

            def endheaders(self, *args, **kwargs):
                return

            def send(self, *args, **kwargs):
                data = kwargs.get('data')
                if data is not None:
                    if hasattr(data, 'read'):
                        data.read()
                    else:
                        for datum in data:
                            pass
                raise socket.error('oops')

            def request(self, *args, **kwargs):
                return

            def getresponse(self, *args, **kwargs):
                self.status = 200
                return self

            def getheader(self, *args, **kwargs):
                return 'header'

            def getheaders(self):
                return [('key1', 'value1'), ('key2', 'value2')]

            def read(self, *args, **kwargs):
                return ''

            def close(self):
                pass

        def local_http_connection(url, proxy=None, cacert=None, insecure=False, cert=None, cert_key=None, ssl_compression=True, timeout=None):
            parsed = urlparse(url)
            return (parsed, LocalConnection())
        with mock.patch.object(c, 'http_connection', local_http_connection):
            conn = c.Connection('http://www.example.com', 'asdf', 'asdf', retries=1, starting_backoff=0.0001)
            contents = LocalContents()
            exc = None
            try:
                conn.put_object('c', 'o', contents)
            except socket.error as err:
                exc = err
            self.assertEqual(contents.tells, [0])
            self.assertEqual(contents.seeks, [(0, 0)])
            self.assertEqual(4, len(contents.reads))
            self.assertEqual((65536, b''), contents.reads[1])
            self.assertEqual((65536, b''), contents.reads[3])
            self.assertEqual(str(exc), 'oops')
            contents = LocalContents(tell_value=123)
            exc = None
            try:
                conn.put_object('c', 'o', contents)
            except socket.error as err:
                exc = err
            self.assertEqual(contents.tells, [123])
            self.assertEqual(contents.seeks, [(123, 0)])
            self.assertEqual(4, len(contents.reads))
            self.assertEqual((65536, b''), contents.reads[1])
            self.assertEqual((65536, b''), contents.reads[3])
            self.assertEqual(str(exc), 'oops')
            contents = LocalContents(tell_value=123)
            wrapped_contents = swiftclient.utils.LengthWrapper(contents, 6, md5=True)
            exc = None
            try:
                conn.put_object('c', 'o', wrapped_contents)
            except socket.error as err:
                exc = err
            self.assertEqual(contents.tells, [123])
            self.assertEqual(contents.seeks, [(123, 0)])
            self.assertEqual(contents.reads, [(6, b'tuvwxy')] * 2)
            self.assertEqual(str(exc), 'oops')
            self.assertEqual(md5(b'tuvwxy').hexdigest(), wrapped_contents.get_md5sum())
            contents = LocalContents()
            contents.tell = None
            exc = None
            try:
                conn.put_object('c', 'o', contents)
            except c.ClientException as err:
                exc = err
            self.assertEqual(contents.seeks, [])
            self.assertEqual(str(exc), "put_object('c', 'o', ...) failure and no ability to reset contents for reupload.")

    def test_get_container(self):
        headers = {'X-Favourite-Pet': 'Aardvark'}
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200, body=b'{}')):
            with mock.patch('swiftclient.client.get_auth', lambda *a, **k: ('http://url:8080/v1/a', 'token')):
                conn = c.Connection()
                conn.get_container('c1', prefix='p', limit=5, headers=headers)
        self.assertEqual(1, len(self.request_log), self.request_log)
        self.assertRequests([('GET', '/v1/a/c1?format=json&limit=5&prefix=p', '', {'x-auth-token': 'token', 'X-Favourite-Pet': 'Aardvark', 'accept-encoding': 'gzip'})])
        self.assertEqual(conn.attempts, 1)

    def test_head_container(self):
        headers = {'X-Favourite-Pet': 'Aardvark'}
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200, body=b'{}')):
            with mock.patch('swiftclient.client.get_auth', lambda *a, **k: ('http://url:8080/v1/a', 'token')):
                conn = c.Connection()
                conn.head_container('c1', headers=headers)
        self.assertEqual(1, len(self.request_log), self.request_log)
        self.assertRequests([('HEAD', '/v1/a/c1', '', {'x-auth-token': 'token', 'X-Favourite-Pet': 'Aardvark'})])
        self.assertEqual(conn.attempts, 1)

    def test_head_object(self):
        headers = {'X-Favourite-Pet': 'Aardvark'}
        query_string = 'foo=bar'
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
            with mock.patch('swiftclient.client.get_auth', lambda *a, **k: ('http://url:8080/v1/a', 'token')):
                conn = c.Connection()
                conn.head_object('c1', 'o1', headers=headers, query_string=query_string)
        self.assertEqual(1, len(self.request_log), self.request_log)
        self.assertRequests([('HEAD', '/v1/a/c1/o1?foo=bar', '', {'x-auth-token': 'token', 'X-Favourite-Pet': 'Aardvark'})])
        self.assertEqual(conn.attempts, 1)

class TestResponseDict(MockHttpTest):
    """
    Verify handling of optional response_dict argument.
    """
    calls = [('post_account', {}), ('post_container', 'c', {}), ('put_container', 'c'), ('delete_container', 'c'), ('post_object', 'c', 'o', {}), ('put_object', 'c', 'o', 'body'), ('copy_object', 'c', 'o'), ('delete_object', 'c', 'o')]

    def fake_get_auth(*args, **kwargs):
        return ('http://url', 'token')

    def test_response_dict_with_auth_error(self):

        def bad_get_auth(*args, **kwargs):
            raise c.ClientException('test')
        for call in self.calls:
            resp_dict = {'test': 'should be untouched'}
            with mock.patch('swiftclient.client.get_auth', bad_get_auth):
                conn = c.Connection('http://127.0.0.1:8080', 'user', 'key')
                self.assertRaises(c.ClientException, getattr(conn, call[0]), *call[1:], response_dict=resp_dict)
            self.assertEqual({'test': 'should be untouched'}, resp_dict)

    def test_response_dict_with_request_error(self):
        for call in self.calls:
            resp_dict = {'test': 'should be untouched'}
            with mock.patch('swiftclient.client.get_auth', self.fake_get_auth):
                exc = c.ClientException('test')
                with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200, exc=exc)):
                    conn = c.Connection('http://127.0.0.1:8080', 'user', 'key')
                    self.assertRaises(c.ClientException, getattr(conn, call[0]), *call[1:], response_dict=resp_dict)
            self.assertEqual('should be untouched', resp_dict.get('test'))
            self.assertEqual([{}], resp_dict.get('response_dicts'))

    def test_response_dict(self):
        for call in self.calls:
            resp_dict = {'test': 'should be untouched'}
            with mock.patch('swiftclient.client.get_auth', self.fake_get_auth):
                with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
                    conn = c.Connection('http://127.0.0.1:8080', 'user', 'key')
                    getattr(conn, call[0])(*call[1:], response_dict=resp_dict)
            self.assertEqual('should be untouched', resp_dict.pop('test', None))
            self.assertEqual('Fake', resp_dict.get('reason'))
            self.assertEqual(200, resp_dict.get('status'))
            self.assertIn('headers', resp_dict)
            self.assertEqual('yes', resp_dict['headers'].get('x-works'))
            children = resp_dict.pop('response_dicts', [])
            self.assertEqual(1, len(children))
            self.assertEqual(resp_dict, children[0])

    def test_response_dict_with_existing(self):
        for call in self.calls:
            resp_dict = {'test': 'should be untouched', 'response_dicts': [{'existing': 'response dict'}]}
            with mock.patch('swiftclient.client.get_auth', self.fake_get_auth):
                with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
                    conn = c.Connection('http://127.0.0.1:8080', 'user', 'key')
                    getattr(conn, call[0])(*call[1:], response_dict=resp_dict)
            self.assertEqual('should be untouched', resp_dict.pop('test', None))
            self.assertEqual('Fake', resp_dict.get('reason'))
            self.assertEqual(200, resp_dict.get('status'))
            self.assertIn('headers', resp_dict)
            self.assertEqual('yes', resp_dict['headers'].get('x-works'))
            children = resp_dict.pop('response_dicts', [])
            self.assertEqual(2, len(children))
            self.assertEqual({'existing': 'response dict'}, children[0])
            self.assertEqual(resp_dict, children[1])

class TestLogging(MockHttpTest):
    """
    Make sure all the lines in http_log are covered.
    """

    def setUp(self):
        super(TestLogging, self).setUp()
        self.swiftclient_logger = logging.getLogger('swiftclient')
        self.log_level = self.swiftclient_logger.getEffectiveLevel()
        self.swiftclient_logger.setLevel(logging.INFO)

    def tearDown(self):
        self.swiftclient_logger.setLevel(self.log_level)
        super(TestLogging, self).tearDown()

    def test_put_ok(self):
        c.http_connection = self.fake_http_connection(200)
        args = ('http://www.test.com', 'asdf', 'asdf', 'asdf', 'asdf')
        value = c.put_object(*args)
        self.assertIsInstance(value, str)

    def test_head_error(self):
        c.http_connection = self.fake_http_connection(500)
        self.assertRaises(c.ClientException, c.head_object, 'http://www.test.com', 'asdf', 'asdf', 'asdf')

    def test_get_error(self):
        c.http_connection = self.fake_http_connection(404)
        with self.assertRaises(c.ClientException) as exc_context:
            c.get_object('http://www.test.com', 'asdf', 'asdf', 'asdf')
        self.assertEqual(exc_context.exception.http_status, 404)

    def test_content_encoding_gzip_body_is_logged_decoded(self):
        buf = io.BytesIO()
        gz = gzip.GzipFile(fileobj=buf, mode='w')
        data = {'test': '☃'}
        decoded_body = json.dumps(data).encode('utf-8')
        gz.write(decoded_body)
        gz.close()
        body = buf.getvalue()
        headers = {'content-encoding': 'gzip'}
        stub_response = StubResponse(500, body, headers)
        with mock.patch('swiftclient.client.logger.info') as mock_log:
            c.http_connection = self.fake_http_connection(stub_response)
            with self.assertRaises(c.ClientException) as exc_context:
                c.get_object('http://www.test.com', 'asdf', 'asdf', 'asdf')
            self.assertEqual(exc_context.exception.http_status, 500)
        self.assertEqual([mock.call('REQ: %s', 'curl -i http://www.test.com/asdf/asdf -X GET -H "X-Auth-Token: ..."'), mock.call('RESP STATUS: %s %s', 500, 'Fake'), mock.call('RESP HEADERS: %s', {'content-encoding': 'gzip'}), mock.call('RESP BODY: %s', decoded_body)], mock_log.mock_calls)

    def test_redact_token(self):
        with mock.patch('swiftclient.client.logger.debug') as mock_log:
            token_value = 'tkee96b40a8ca44fc5ad72ec5a7c90d9b'
            token_encoded = token_value.encode('utf8')
            unicode_token_value = '天空中的乌云天空中的乌云天空中的乌'
            unicode_token_encoded = unicode_token_value.encode('utf8')
            set_cookie_value = 'X-Auth-Token=%s' % token_value
            set_cookie_encoded = set_cookie_value.encode('utf8')
            c.http_log(['GET'], {'headers': {'X-Auth-Token': token_encoded, 'X-Storage-Token': unicode_token_encoded}}, MockHttpResponse(status=200, headers={'X-Auth-Token': token_encoded, 'X-Storage-Token': unicode_token_encoded, 'Etag': b'mock_etag', 'Set-Cookie': set_cookie_encoded}), '')
            out = []
            for _, args, kwargs in mock_log.mock_calls:
                for arg in args:
                    out.append('%s' % arg)
            output = ''.join(out)
            self.assertIn('X-Auth-Token', output)
            self.assertIn(token_value[:16] + '...', output)
            self.assertIn('X-Storage-Token', output)
            self.assertIn(unicode_token_value[:8] + '...', output)
            self.assertIn('Set-Cookie', output)
            self.assertIn(set_cookie_value[:16] + '...', output)
            self.assertNotIn(token_value, output)
            self.assertNotIn(unicode_token_value, output)
            self.assertNotIn(set_cookie_value, output)

    def test_show_token(self):
        with mock.patch('swiftclient.client.logger.debug') as mock_log:
            token_value = 'tkee96b40a8ca44fc5ad72ec5a7c90d9b'
            token_encoded = token_value.encode('utf8')
            unicode_token_value = '天空中的乌云天空中的乌云天空中的乌'
            c.logger_settings['redact_sensitive_headers'] = False
            unicode_token_encoded = unicode_token_value.encode('utf8')
            c.http_log(['GET'], {'headers': {'X-Auth-Token': token_encoded, 'X-Storage-Token': unicode_token_encoded}}, MockHttpResponse(status=200, headers=[('X-Auth-Token', token_encoded), ('X-Storage-Token', unicode_token_encoded), ('Etag', b'mock_etag')]), '')
            out = []
            for _, args, kwargs in mock_log.mock_calls:
                for arg in args:
                    out.append('%s' % arg)
            output = ''.join(out)
            self.assertIn('X-Auth-Token', output)
            self.assertIn(token_value, output)
            self.assertIn('X-Storage-Token', output)
            self.assertIn(unicode_token_value, output)

    @mock.patch('swiftclient.client.logger.debug')
    def test_unicode_path(self, mock_log):
        path = 'http://swift/v1/AUTH_account-ت'.encode('utf-8')
        c.http_log(['GET', path], {}, MockHttpResponse(status=200, headers=[]), '')
        request_log_line = mock_log.mock_calls[0]
        self.assertEqual('REQ: %s', request_log_line[1][0])
        self.assertEqual('curl -i -X GET %s' % path.decode('utf-8'), request_log_line[1][1])

class TestCloseConnection(MockHttpTest):

    def test_close_none(self):
        c.http_connection = self.fake_http_connection()
        conn = c.Connection('http://www.test.com', 'asdf', 'asdf')
        self.assertIsNone(conn.http_conn)
        conn.close()
        self.assertIsNone(conn.http_conn)
        conn.close()
        self.assertIsNone(conn.http_conn)

    def test_close_ok(self):
        url = 'http://www.test.com'
        conn = c.Connection(url, 'asdf', 'asdf')
        self.assertIsNone(conn.http_conn)
        conn.http_conn = c.http_connection(url)
        self.assertEqual(type(conn.http_conn), tuple)
        self.assertEqual(len(conn.http_conn), 2)
        http_conn_obj = conn.http_conn[1]
        self.assertIsInstance(http_conn_obj, c.HTTPConnection)
        self.assertTrue(hasattr(http_conn_obj, 'close'))
        conn.close()

class TestServiceToken(MockHttpTest):

    def setUp(self):
        super(TestServiceToken, self).setUp()
        self.os_options = {'object_storage_url': 'http://storage_url.com', 'service_username': 'service_username', 'service_project_name': 'service_project_name', 'service_key': 'service_key'}

    def get_connection(self):
        conn = c.Connection('http://www.test.com', 'asdf', 'asdf', os_options=self.os_options)
        self.assertIs(type(conn), c.Connection)
        conn.get_auth = self.get_auth
        conn.get_service_auth = self.get_service_auth
        self.assertEqual(conn.attempts, 0)
        self.assertIsNone(conn.service_token)
        self.assertIs(type(conn), c.Connection)
        return conn

    def get_auth(self):
        return (self.os_options.get('object_storage_url'), 'token')

    def get_service_auth(self):
        return (self.os_options.get('object_storage_url'), 'stoken')

    def test_service_token_reauth(self):
        get_auth_call_list = []

        def get_auth(url, user, key, **kwargs):
            args = {'url': url, 'user': user, 'key': key, 'kwargs': kwargs}
            get_auth_call_list.append(args)
            return_dict = {'asdf': 'new', 'service_username': 'newserv'}
            storage_url = kwargs['os_options'].get('object_storage_url')
            return (storage_url, return_dict[user])

        def swap_sleep(*args):
            self.swap_sleep_called = True
            c.get_auth = get_auth
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(401, 200)):
            with mock.patch('swiftclient.client.sleep', swap_sleep):
                self.swap_sleep_called = False
                conn = c.Connection('http://www.test.com', 'asdf', 'asdf', preauthurl='http://www.old.com', preauthtoken='old', os_options=self.os_options)
                self.assertEqual(conn.attempts, 0)
                self.assertEqual(conn.url, 'http://www.old.com')
                self.assertEqual(conn.token, 'old')
                conn.head_account()
        self.assertTrue(self.swap_sleep_called)
        self.assertEqual(conn.attempts, 2)
        self.assertEqual(conn.url, 'http://www.old.com')
        self.assertEqual(conn.token, 'new')
        self.assertEqual(conn.service_token, 'newserv')
        auth_args = get_auth_call_list[0]
        auth_kwargs = get_auth_call_list[0]['kwargs']
        self.assertEqual('asdf', auth_args['user'])
        self.assertEqual('asdf', auth_args['key'])
        self.assertEqual('service_key', auth_kwargs['os_options']['service_key'])
        self.assertEqual('service_username', auth_kwargs['os_options']['service_username'])
        self.assertEqual('service_project_name', auth_kwargs['os_options']['service_project_name'])
        auth_args = get_auth_call_list[1]
        auth_kwargs = get_auth_call_list[1]['kwargs']
        self.assertEqual('service_username', auth_args['user'])
        self.assertEqual('service_key', auth_args['key'])
        self.assertEqual('service_project_name', auth_kwargs['os_options']['tenant_name'])

    def test_service_token_reauth_retries_0(self):
        get_auth_call_list = []

        def get_auth(url, user, key, **kwargs):
            args = {'url': url, 'user': user, 'key': key, 'kwargs': kwargs}
            get_auth_call_list.append(args)
            return_dict = {'asdf': 'new', 'service_username': 'newserv'}
            storage_url = kwargs['os_options'].get('object_storage_url')
            return (storage_url, return_dict[user])

        def swap_sleep(*args):
            self.swap_sleep_called = True
            c.get_auth = get_auth
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(401, 200)):
            with mock.patch('swiftclient.client.sleep', swap_sleep):
                self.swap_sleep_called = False
                conn = c.Connection('http://www.test.com', 'asdf', 'asdf', preauthurl='http://www.old.com', preauthtoken='old', os_options=self.os_options, retries=0)
                self.assertEqual(conn.attempts, 0)
                self.assertEqual(conn.url, 'http://www.old.com')
                self.assertEqual(conn.token, 'old')
                conn.head_account()
        self.assertTrue(self.swap_sleep_called)
        self.assertEqual(conn.attempts, 2)
        self.assertEqual(conn.url, 'http://www.old.com')
        self.assertEqual(conn.token, 'new')
        self.assertEqual(conn.service_token, 'newserv')
        auth_args = get_auth_call_list[0]
        auth_kwargs = get_auth_call_list[0]['kwargs']
        self.assertEqual('asdf', auth_args['user'])
        self.assertEqual('asdf', auth_args['key'])
        self.assertEqual('service_key', auth_kwargs['os_options']['service_key'])
        self.assertEqual('service_username', auth_kwargs['os_options']['service_username'])
        self.assertEqual('service_project_name', auth_kwargs['os_options']['service_project_name'])
        auth_args = get_auth_call_list[1]
        auth_kwargs = get_auth_call_list[1]['kwargs']
        self.assertEqual('service_username', auth_args['user'])
        self.assertEqual('service_key', auth_args['key'])
        self.assertEqual('service_project_name', auth_kwargs['os_options']['tenant_name'])
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(401, 401, 401, 401)):
            with mock.patch('swiftclient.client.sleep', swap_sleep):
                self.swap_sleep_called = False
                conn = c.Connection('http://www.test.com', 'asdf', 'asdf', preauthurl='http://www.old.com', preauthtoken='old', os_options=self.os_options, retries=0)
                self.assertEqual(conn.attempts, 0)
                self.assertRaises(c.ClientException, conn.head_account)
                self.assertEqual(conn.attempts, 2)
                unused_responses = list(self.fake_connect.code_iter)
                self.assertEqual(unused_responses, [401, 401])

    def test_service_token_get_account(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
            with mock.patch('swiftclient.client.parse_api_response'):
                conn = self.get_connection()
                conn.get_account()
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('GET', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/?format=json', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_head_account(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
            conn = self.get_connection()
            conn.head_account()
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('HEAD', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_post_account(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(201)):
            conn = self.get_connection()
            conn.post_account(headers={})
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('POST', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_delete_container(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(204)):
            conn = self.get_connection()
            conn.delete_container('container1')
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('DELETE', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/container1', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_get_container(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
            with mock.patch('swiftclient.client.parse_api_response'):
                conn = self.get_connection()
                conn.get_container('container1')
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('GET', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/container1?format=json', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_get_container_full_listing(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200, 200)):
            with mock.patch('swiftclient.client.parse_api_response') as resp:
                resp.side_effect = ([{'name': 'obj1'}], [])
                conn = self.get_connection()
                conn.get_container('container1', full_listing=True)
        self.assertEqual(2, len(self.request_log), self.request_log)
        expected_urls = iter(('http://storage_url.com/container1?format=json', 'http://storage_url.com/container1?format=json&marker=obj1'))
        for actual in self.iter_request_log():
            self.assertEqual('GET', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual(next(expected_urls), actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_head_container(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
            conn = self.get_connection()
            conn.head_container('container1')
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('HEAD', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/container1', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_post_container(self):
        headers = {'X-Container-Meta-Color': 'blue'}
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(201)):
            conn = self.get_connection()
            conn.post_container('container1', headers)
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('POST', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/container1', actual['full_path'])
        self.assertEqual(conn.attempts, 1)
        self.assertEqual(headers, {'X-Container-Meta-Color': 'blue'})

    def test_service_token_put_container(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
            conn = self.get_connection()
            conn.put_container('container1')
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('PUT', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/container1', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_get_object(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
            conn = self.get_connection()
            conn.get_object('container1', 'obj1')
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('GET', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/container1/obj1', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_head_object(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
            conn = self.get_connection()
            conn.head_object('container1', 'obj1')
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('HEAD', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/container1/obj1', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_put_object(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(200)):
            conn = self.get_connection()
            conn.put_object('container1', 'obj1', 'a_string')
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('PUT', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/container1/obj1', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_post_object(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(202)):
            conn = self.get_connection()
            conn.post_object('container1', 'obj1', {})
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('POST', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/container1/obj1', actual['full_path'])
        self.assertEqual(conn.attempts, 1)

    def test_service_token_delete_object(self):
        with mock.patch('swiftclient.client.http_connection', self.fake_http_connection(202)):
            conn = self.get_connection()
            conn.delete_object('container1', 'obj1', query_string='a_string')
        self.assertEqual(1, len(self.request_log), self.request_log)
        for actual in self.iter_request_log():
            self.assertEqual('DELETE', actual['method'])
            actual_hdrs = actual['headers']
            self.assertEqual('stoken', actual_hdrs.get('X-Service-Token'))
            self.assertEqual('token', actual_hdrs['X-Auth-Token'])
            self.assertEqual('http://storage_url.com/container1/obj1?a_string', actual['full_path'])
        self.assertEqual(conn.attempts, 1)