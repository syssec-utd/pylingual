import re
import sys
from smscx_client.api_client import ApiClient, Endpoint as _Endpoint
from smscx_client.model_utils import check_allowed_values, check_validations, date, datetime, file_type, none_type, validate_and_convert_types
from smscx_client.model.model400_invalid_param import Model400InvalidParam
from smscx_client.model.model401_unauthorized import Model401Unauthorized
from smscx_client.model.model403_insufficient_scope import Model403InsufficientScope
from smscx_client.model.model500_server_error import Model500ServerError
from smscx_client.model.oauth_token_response import OauthTokenResponse

class OauthApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.get_access_token_endpoint = _Endpoint(settings={'response_type': (OauthTokenResponse,), 'auth': ['BasicAuth'], 'endpoint_path': '/oauth/token', 'operation_id': 'get_access_token', 'http_method': 'POST', 'servers': None}, params_map={'all': ['grant_type', 'scope'], 'required': ['grant_type'], 'nullable': [], 'enum': ['grant_type'], 'validation': []}, root_map={'validations': {}, 'allowed_values': {('grant_type',): {'CLIENT_CREDENTIALS': 'client_credentials'}}, 'api_types': {'grant_type': (str,), 'scope': (str,)}, 'attribute_map': {'grant_type': 'grant_type', 'scope': 'scope'}, 'location_map': {'grant_type': 'form', 'scope': 'form'}, 'collection_format_map': {}}, headers_map={'accept': ['application/json'], 'content_type': ['application/x-www-form-urlencoded']}, api_client=api_client)

    def get_access_token(self, grant_type='client_credentials', **kwargs):
        """Get access token  # noqa: E501

        Generate an access token.    The POST request must use the HTTP Basic authentication scheme, by encoding `client_id:client_secret` string to Base64 string and use it in the header:    ```  Authorization: Basic czZCaGRSa3F0Mzo3RmpmcDBaQnIxS3REUmJuZlZkbUl3   ```    The request body should have the mandatory `grant_type` parameter with value `client_credentials`    The content type must be `application/x-www-form-urlencoded`.      
### Errors for POST `/oauth/token`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1600  |  invalid_request  |  The request is missing a required parameter (grant_type) |  

|  400 | 1600  |  invalid_scope  |  The requested scope is invalid, unknown, or malformed |  

|  400 | 1600  |  unsupported_grant_type  |  The grant type is not supported (only client_credentials) |  
|  401 | 1600  |  invalid_client  |  Invalid client |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_access_token(grant_type="client_credentials", async_req=True)
        >>> result = thread.get()

        Args:
            grant_type (str): Grant type (or flow) represents the methods through which the application will get Access Tokens. Must have value `client_credentials`. defaults to "client_credentials", must be one of ["client_credentials"]

        Keyword Args:
            scope (str): A list of space-delimited, case-sensitive strings. If left empty or ommited, the issued access token will be granted with all scopes (full privileges). [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            OauthTokenResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get('async_req', False)
        kwargs['_return_http_data_only'] = kwargs.get('_return_http_data_only', True)
        kwargs['_preload_content'] = kwargs.get('_preload_content', True)
        kwargs['_request_timeout'] = kwargs.get('_request_timeout', None)
        kwargs['_check_input_type'] = kwargs.get('_check_input_type', True)
        kwargs['_check_return_type'] = kwargs.get('_check_return_type', True)
        kwargs['_spec_property_naming'] = kwargs.get('_spec_property_naming', False)
        kwargs['_content_type'] = kwargs.get('_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        kwargs['grant_type'] = grant_type
        return self.get_access_token_endpoint.call_with_http_info(**kwargs)