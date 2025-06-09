import logging
import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
logger = logging.getLogger(__name__)

def create_client(jupyterhub_endpoint, project_name, reuse_existing=True):
    for variable in {'AUTH0_DOMAIN', 'AUTH0_CLIENT_ID', 'AUTH0_CLIENT_SECRET'}:
        if variable not in os.environ:
            raise ValueError(f'Required environment variable={variable} not defined')
    get_token = GetToken(os.environ['AUTH0_DOMAIN'])
    token = get_token.client_credentials(os.environ['AUTH0_CLIENT_ID'], os.environ['AUTH0_CLIENT_SECRET'], f"https://{os.environ['AUTH0_DOMAIN']}/api/v2/")
    mgmt_api_token = token['access_token']
    auth0 = Auth0(os.environ['AUTH0_DOMAIN'], mgmt_api_token)
    oauth_callback_url = f'https://{jupyterhub_endpoint}/auth/realms/nebari/broker/auth0/endpoint'
    for client in auth0.clients.all(fields=['name', 'client_id', 'client_secret', 'callbacks'], include_fields=True):
        if client['name'] == project_name and reuse_existing:
            if oauth_callback_url not in client['callbacks']:
                logger.info(f"updating existing application={project_name} client_id={client['client_id']} adding callback url={oauth_callback_url}")
                auth0.clients.update(client['client_id'], {'callbacks': client['callbacks'] + [oauth_callback_url]})
            return {'auth0_subdomain': '.'.join(os.environ['AUTH0_DOMAIN'].split('.')[:-2]), 'client_id': client['client_id'], 'client_secret': client['client_secret']}
    client = auth0.clients.create({'name': project_name, 'description': f'Nebari - {project_name} - {jupyterhub_endpoint}', 'callbacks': [oauth_callback_url], 'app_type': 'regular_web'})
    return {'auth0_subdomain': '.'.join(os.environ['AUTH0_DOMAIN'].split('.')[:-2]), 'client_id': client['client_id'], 'client_secret': client['client_secret']}