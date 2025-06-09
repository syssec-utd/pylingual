import jwt
from simple_rest_client.api import API
from simple_rest_client.resource import Resource
from sdk.api.utils import expired
CLIENT_ID = 'vgs-cli-public'
SCOPE = 'openid'
env_url = {'dev': 'https://auth.verygoodsecurity.io', 'prod': 'https://auth.verygoodsecurity.com'}

class AuthResource(Resource):
    actions = {'token': {'method': 'POST', 'url': 'auth/realms/vgs/protocol/openid-connect/token'}, 'logout': {'method': 'POST', 'url': 'auth/realms/vgs/protocol/openid-connect/logout'}}

def create_api(environment):
    api = API(api_root_url=env_url[environment], params={}, headers={}, timeout=50, append_slash=False)
    api.add_resource(resource_name='auth', resource_class=AuthResource)
    return api

def get_token(api, code, code_verifier, callback_url):
    return _get_token(api, code=code, code_verifier=str(code_verifier), redirect_uri=callback_url, grant_type='authorization_code', client_id='vgs-cli-public')

def logout(api, client_id, access_token, refresh_token):
    return api.auth.logout(headers={'Authorization': access_token, 'Content-Type': 'application/x-www-form-urlencoded'}, body='client_id={client_id}&refresh_token={refresh_token}'.format(client_id=client_id, refresh_token=refresh_token))

def get_auto_token(api, **kwargs):
    return _get_token(api, grant_type='client_credentials', **kwargs)

def _get_token(api, **kwargs):
    return api.auth.token(body=kwargs)

def refresh_token(api, client_id=None, refresh_token=None):
    client_id = client_id or CLIENT_ID
    payload = {'refresh_token': refresh_token, 'grant_type': 'refresh_token', 'client_id': client_id}
    return api.auth.token(body=payload)

def validate_access_token(auth_token):
    token_json = jwt.decode(auth_token, verify=False)
    return not expired(token_json['exp'])