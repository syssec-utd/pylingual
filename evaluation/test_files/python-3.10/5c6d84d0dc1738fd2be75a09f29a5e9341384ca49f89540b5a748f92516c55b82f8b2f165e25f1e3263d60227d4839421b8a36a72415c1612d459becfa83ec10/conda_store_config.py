import json
import logging
import os
import tempfile
import requests
from conda_store_server import api, orm, schema
from conda_store_server.server.auth import GenericOAuthAuthentication
from conda_store_server.server.dependencies import get_conda_store
from conda_store_server.storage import S3Storage

def conda_store_config(path='/var/lib/conda-store/config.json'):
    with open(path) as f:
        return json.load(f)
config = conda_store_config()
c.CondaStore.storage_class = S3Storage
c.CondaStore.store_directory = '/home/conda/'
c.CondaStore.database_url = f"postgresql+psycopg2://{config['postgres-username']}:{config['postgres-password']}@{config['postgres-service']}/conda-store"
c.CondaStore.redis_url = f"redis://:{config['redis-password']}@{config['redis-service']}:6379/0"
c.CondaStore.default_uid = 1000
c.CondaStore.default_gid = 100
c.CondaStore.default_permissions = '775'
c.CondaStore.conda_included_packages = ['ipykernel']
c.S3Storage.internal_endpoint = f"{config['minio-service']}:9000"
c.S3Storage.internal_secure = False
c.S3Storage.external_endpoint = f"{config['external-url']}:9080"
c.S3Storage.external_secure = True
c.S3Storage.access_key = config['minio-username']
c.S3Storage.secret_key = config['minio-password']
c.S3Storage.region = 'us-east-1'
c.S3Storage.bucket_name = 'conda-store'
c.CondaStore.default_namespace = 'global'
c.CondaStore.filesystem_namespace = config['default-namespace']
c.CondaStoreServer.log_level = logging.INFO
c.CondaStoreServer.enable_ui = True
c.CondaStoreServer.enable_api = True
c.CondaStoreServer.enable_registry = True
c.CondaStoreServer.enable_metrics = True
c.CondaStoreServer.address = '0.0.0.0'
c.CondaStoreServer.port = 5000
c.CondaStoreServer.behind_proxy = True
c.CondaStoreServer.url_prefix = '/conda-store'
c.GenericOAuthAuthentication.access_token_url = config['openid-config']['token_url']
c.GenericOAuthAuthentication.authorize_url = config['openid-config']['authentication_url']
c.GenericOAuthAuthentication.user_data_url = config['openid-config']['userinfo_url']
c.GenericOAuthAuthentication.oauth_callback_url = f"https://{config['external-url']}/conda-store/oauth_callback"
c.GenericOAuthAuthentication.client_id = config['openid-config']['client_id']
c.GenericOAuthAuthentication.client_secret = config['openid-config']['client_secret']
c.GenericOAuthAuthentication.access_scope = 'profile'
c.GenericOAuthAuthentication.user_data_key = 'preferred_username'
c.GenericOAuthAuthentication.tls_verify = False

class KeyCloakAuthentication(GenericOAuthAuthentication):

    async def authenticate(self, request):
        oauth_access_token = self._get_oauth_token(request)
        if oauth_access_token is None:
            return None
        response = requests.get(self.user_data_url, headers={'Authorization': f'Bearer {oauth_access_token}'}, verify=self.tls_verify)
        response.raise_for_status()
        user_data = response.json()
        role_mappings = {'conda_store_admin': 'admin', 'conda_store_developer': 'developer', 'conda_store_viewer': 'viewer'}
        roles = {role_mappings[role] for role in user_data.get('roles', []) if role in role_mappings}
        username = user_data['preferred_username']
        default_namespace = config['default-namespace']
        namespaces = {username, 'global', default_namespace}
        role_bindings = {f'{username}/*': {'admin'}, f'{default_namespace}/*': {'viewer'}, 'global/*': roles}
        for group in user_data.get('groups', []):
            group_name = os.path.basename(group)
            namespaces.add(group_name)
            role_bindings[f'{group_name}/*'] = roles
        conda_store = get_conda_store(request)
        for namespace in namespaces:
            _namespace = api.get_namespace(conda_store.db, name=namespace)
            if _namespace is None:
                conda_store.db.add(orm.Namespace(name=namespace))
                conda_store.db.commit()
        return schema.AuthenticationToken(primary_namespace=username, role_bindings=role_bindings)
c.CondaStoreServer.authentication_class = KeyCloakAuthentication
c.AuthenticationBackend.predefined_tokens = {service_token: service_permissions for (service_token, service_permissions) in config['service-tokens'].items()}
c.CondaStoreWorker.log_level = logging.INFO
c.CondaStoreWorker.watch_paths = ['/opt/environments']
c.CondaStoreWorker.concurrency = 4
c.CondaStore.environment_directory = '/home/conda/{namespace}/envs/{namespace}-{name}'
conda_store_settings = config['extra-settings']
for (classname, attributes) in conda_store_settings.items():
    for (attribute, value) in attributes.items():
        setattr(getattr(c, classname), attribute, value)
extra_config_filename = os.path.join(tempfile.gettempdir(), 'extra-config.py')
extra_config = config.get('extra-config', '')
with open(extra_config_filename, 'w') as f:
    f.write(extra_config)
exec(compile(source=extra_config, filename=extra_config_filename, mode='exec'))