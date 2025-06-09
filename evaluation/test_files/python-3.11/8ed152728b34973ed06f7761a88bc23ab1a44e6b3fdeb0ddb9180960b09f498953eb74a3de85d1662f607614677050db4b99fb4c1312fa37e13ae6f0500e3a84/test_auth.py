from unittest import mock
from unittest import TestCase
from mercuryclient.api import MercuryApi

class AuthMixinTest(TestCase):

    def setUp(self):
        self.post_api_mock = mock.patch('mercuryclient.api.MercuryApi._post_json_http_request').start()
        self.addCleanup(self.post_api_mock.stop)

    def test_authorizing_client(self):
        client = MercuryApi({'username': 'username', 'password': 'password', 'url': 'https://mercury-dev.esthenos.in'})
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json = mock.MagicMock()
        mock_response.json.return_value = {'refresh': 'refresh_token', 'access': 'access_token'}
        self.post_api_mock.return_value = ('random_string', mock_response)
        client._authorize_client()
        self.post_api_mock.assert_called_with('api/v1/token/', data={'username': 'username', 'password': 'password'}, send_request_id=True, add_bearer_token=False)
        self.post_api_mock.reset_mock()
        mock_response = mock.MagicMock()
        mock_response.status_code = 403
        self.post_api_mock.return_value = ('random_string', mock_response)
        with self.assertRaises(Exception):
            client._authorize_client()
        self.post_api_mock.assert_called_with('api/v1/token/', data={'username': 'username', 'password': 'password'}, send_request_id=True, add_bearer_token=False)

    def test_refreshing_access_token(self):
        client = MercuryApi({'username': 'username', 'password': 'password', 'url': 'https://mercury-dev.esthenos.in'})
        client._refresh_token = 'refresh_token'
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json = mock.MagicMock()
        mock_response.json.return_value = {'access': 'access_token'}
        self.post_api_mock.return_value = ('random_string', mock_response)
        client.set_access_token()
        self.post_api_mock.assert_called_with('api/v1/token/refresh/', data={'refresh': 'refresh_token'}, send_request_id=True, add_bearer_token=False)
        self.post_api_mock.reset_mock()
        mock_response = mock.MagicMock()
        mock_response.status_code = 403
        self.post_api_mock.return_value = ('random_string', mock_response)
        with self.assertRaises(Exception):
            client.set_access_token()
        self.post_api_mock.assert_called_with('api/v1/token/refresh/', data={'refresh': 'refresh_token'}, send_request_id=True, add_bearer_token=False)