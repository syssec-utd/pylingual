import importlib.resources as pkg_resources
import os
import tempfile
import textwrap
import uuid
from string import Template
import requests
import vgs.exceptions
import vgscli.auth
import vgscli.routes
import vgscli.vaults_api
from requests import utils
from simple_rest_client.exceptions import NotFoundError
from vgs import certs
from vgs.configuration import Configuration
from vgscli.auth import token_util
from vgscli.errors import RouteNotValidError
USER_AGENT = 'vgs-api-client/0.0.1-dev202207081533/python'
ECHO_SECURE_HOST_CONFIG = 'echo\\.secure\\.verygood\\.systems'
FUNCTION_CONDITION_EXPRESSION = "'field': 'QueryString', 'type': 'string', 'operator': 'equals', 'values': ['function_name="
FUNCTION_TYPE_LARKY = 'larky'
ROUTE_TEMPLATE = '\ndata:\n  - attributes:\n      destination_override_endpoint: \'*\'\n      entries:\n        - id: ${function_filter}\n          config:\n            condition: AND\n            rules:\n              - expression:\n                  field: PathInfo\n                  operator: equals\n                  type: string\n                  values:\n                    - /post\n              - expression:\n                  field: QueryString\n                  operator: equals\n                  type: string\n                  values:\n                    - function_name=${name}\n          operation: REDACT\n          operations:\n            - - name: github.com/verygoodsecurity/common/compute/larky/http/Process\n                parameters:\n                  script: |-\n                    ${definition}\n          phase: REQUEST\n          public_token_generator: UUID\n          targets:\n            - body\n          token_manager: PERSISTENT\n          transformer: JSON_PATH\n          transformer_config:\n            - none\n          classifiers: {}\n        - id: ${execution_flag_filter}\n          config:\n            condition: AND\n            rules:\n              - expression:\n                  field: PathInfo\n                  operator: equals\n                  type: string\n                  values:\n                    - /post\n              - expression:\n                  field: QueryString\n                  operator: equals\n                  type: string\n                  values:\n                    - function_name=${name}\n          operation: REDACT\n          operations:\n            - - name: github.com/verygoodsecurity/common/compute/larky/http/Process\n                parameters:\n                  script: |-\n                    load("@stdlib//builtins", "builtins")\n\n                    def process(input, ctx):\n                        headers = input.headers\n                        headers["X-VGS-Function"] = "True"\n                        input.headers = headers\n                        return input\n          phase: RESPONSE\n          public_token_generator: UUID\n          targets:\n            - body\n          token_manager: PERSISTENT\n          transformer: JSON_PATH\n          transformer_config:\n            - none\n          classifiers: {}\n      host_endpoint: echo\\.secure\\.verygood\\.systems\n      port: 80\n      protocol: http\n      source_endpoint: \'*\'\n      tags:\n        name: ${name}\n    id: ${route_id}\n    type: rule_chain\nversion: 1\n'

class Functions:

    def __init__(self, config: Configuration):
        self.config = config
        self.proxy_cert = None
        self.auth_server_environment = 'dev' if config.environment == 'dev' else 'prod'

    def create(self, name, language, definition):
        if not name:
            raise vgs.exceptions.FunctionsApiException('Function name is required')
        if language != FUNCTION_TYPE_LARKY:
            raise vgs.exceptions.FunctionsApiException(f'Unsupported function type. Supported types: {FUNCTION_TYPE_LARKY}')
        self._authenticate()
        route_id = self._function_id(name)
        route_definition = Template(ROUTE_TEMPLATE).substitute(name=name, definition=self._indent_definition(definition), route_id=route_id, function_filter=uuid.uuid4(), execution_flag_filter=uuid.uuid4())
        self._create_route(route_definition)

    def list(self):
        self._authenticate()
        try:
            routes = self._list_routes()
            return list(self._extract_functions(routes))
        except Exception as ex:
            raise vgs.FunctionsApiException(f'Failed to list functions') from ex

    def get(self, name):
        if not name:
            raise vgs.exceptions.FunctionsApiException('Function name is required')
        self._authenticate()
        route_id = self._function_id(name)
        try:
            route_config = self._get_route(route_id)
            definition = self._extract_larky(route_config)
        except NotFoundError as nfe:
            raise vgs.NotFoundException(f"Function '{name}' not found")
        except Exception as ex:
            raise vgs.FunctionsApiException(f"Failed to get '{name}' function") from ex
        return (name, FUNCTION_TYPE_LARKY, definition)

    def delete(self, name):
        if not name:
            raise vgs.exceptions.FunctionsApiException('Function name is required')
        self._authenticate()
        route_id = self._function_id(name)
        try:
            self._delete_route(route_id)
        except NotFoundError:
            raise vgs.NotFoundException(f"Function '{name}' not found")
        except Exception as ex:
            raise vgs.FunctionsApiException(f"Failed to delete '{name}' function") from ex

    def _authenticate(self):
        if not (self.config.service_account_name and self.config.service_account_password):
            raise vgs.exceptions.FunctionsApiException("Functions API configuration is not complete. Please set 'service_account_name' and 'service_account_password' to use functions CRUD API.")
        vgscli.auth.client_credentials_login(None, self.config.service_account_name, self.config.service_account_password, self.auth_server_environment)
        vgscli.auth.handshake(None, self.auth_server_environment)

    @staticmethod
    def _extract_larky(route_config):
        script = route_config['attributes']['entries'][0]['operations'][0][0]['parameters']['script']
        return script

    @staticmethod
    def _extract_functions(routes):
        for route in routes:
            try:
                host_endpoint = route['attributes']['host_endpoint']
                filter_config = str(route['attributes']['entries'][0]['config'])
                if host_endpoint == ECHO_SECURE_HOST_CONFIG and FUNCTION_CONDITION_EXPRESSION in filter_config:
                    function_name = route['attributes']['tags']['name']
                    yield function_name
            except Exception as e:
                continue

    @staticmethod
    def _indent_definition(definition):
        dedented = textwrap.dedent(definition)
        return textwrap.indent(dedented, '                    ')

    @staticmethod
    def _function_id(name):
        return uuid.uuid5(uuid.NAMESPACE_URL, f'https://echo.secure.verygood.systems/post?function_name={name}')

    @staticmethod
    def _get_proxy_host(environment):
        return {'live': 'live.verygoodproxy.com', 'live-eu-1': 'live-eu-1.verygoodproxy.com', 'sandbox': 'sandbox.verygoodproxy.com', 'dev': 'sandbox.verygoodproxy.io'}.get(environment, 'sandbox.verygoodproxy.com')

    @staticmethod
    def _get_proxy_cert(environment):
        return {'live': pkg_resources.read_text(certs, 'vgs-proxy-live.pem'), 'live-eu-1': pkg_resources.read_text(certs, 'vgs-proxy-live.pem'), 'sandbox': pkg_resources.read_text(certs, 'vgs-proxy-sandbox.pem'), 'dev': pkg_resources.read_text(certs, 'vgs-proxy-dev.pem')}.get(environment, pkg_resources.read_text(certs, 'vgs-proxy-sandbox.pem'))

    def _load_cert(self, environment):
        proxy_cert = self._get_proxy_cert(environment)
        path_to_lib_ca = utils.DEFAULT_CA_BUNDLE_PATH
        return str.encode(proxy_cert) + str.encode(os.linesep) + self._read_file(path_to_lib_ca)

    @staticmethod
    def _read_file(path):
        with open(path, mode='rb') as file:
            return file.read()

    def _create_route(self, route_definition):
        routes_api = self._create_routes_api()
        try:
            vgscli.routes.sync_all_routes(routes_api, route_definition)
        except RouteNotValidError as routeError:
            raise vgs.exceptions.FunctionsApiException(routeError.message)

    def _get_route(self, route_id):
        routes_api = self._create_routes_api()
        response = routes_api.routes.retrieve(route_id)
        return response.body['data']

    def _list_routes(self):
        routes_api = self._create_routes_api()
        response = routes_api.routes.list()
        return response.body['data']

    def _delete_route(self, route_id):
        routes_api = self._create_routes_api()
        return routes_api.routes.delete(route_id)

    def _create_routes_api(self):
        auth_token = token_util.get_access_token()
        api = vgscli.vaults_api.create_api(None, self.config.vault_id, self.auth_server_environment, auth_token)
        api.headers['User-Agent'] = USER_AGENT
        return api

    def invoke(self, name, data):
        if not (self.config.username and self.config.password):
            raise vgs.exceptions.FunctionsApiException("Functions API configuration is not complete. Please set access credentials ('username' and 'password') to use functions invocation API.")
        if not self.config.vault_id:
            raise vgs.exceptions.FunctionsApiException("Functions API configuration is not complete. Please set 'vault_id' to use functions invocation API.")
        username = self.config.username
        password = self.config.password
        vault_id = self.config.vault_id
        proxy_host = self._get_proxy_host(self.config.environment)
        if not self.proxy_cert:
            self.proxy_cert = self._load_cert(self.config.environment)
        headers = {'User-Agent': USER_AGENT}
        with tempfile.NamedTemporaryFile() as ca_file:
            ca_file.write(self.proxy_cert)
            response = requests.post(f'https://echo.secure.verygood.systems/post?function_name={name}', proxies={'https': f'https://{username}:{password}@{vault_id}.{proxy_host}:8443'}, data=data, headers=headers, verify=ca_file.name)
        if response.status_code != 200:
            raise vgs.FunctionsApiException(f"Failed to invoke function '{name}'. Reason: {response.content}")
        if response.headers.get('X-VGS-Function') != 'True':
            raise vgs.FunctionsApiException(f"Function '{name}' doesn't exist.")
        return response.content