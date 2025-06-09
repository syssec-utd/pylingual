import functools
import json
import os
from aiohttp import web
from dask_gateway_server.auth import JupyterHubAuthenticator
from dask_gateway_server.options import Mapping, Options, Select

def dask_gateway_config(path='/var/lib/dask-gateway/config.json'):
    with open(path) as f:
        return json.load(f)
config = dask_gateway_config()
c.DaskGateway.log_level = config['gateway']['loglevel']
c.DaskGateway.address = ':8000'
c.KubeBackend.api_url = f"http://{config['gateway_service_name']}.{config['gateway_service_namespace']}:8000/api"
c.DaskGateway.backend_class = 'dask_gateway_server.backends.kubernetes.KubeBackend'
c.KubeBackend.gateway_instance = config['gateway_service_name']
c.KubeClusterConfig.image = f"{config['cluster-image']['name']}:{config['cluster-image']['tag']}"
c.KubeClusterConfig.image_pull_policy = config['cluster']['image_pull_policy']
c.KubeClusterConfig.environment = config['cluster']['environment']
c.KubeClusterConfig.idle_timeout = config['cluster']['idle_timeout']
c.KubeClusterConfig.scheduler_cores = config['cluster']['scheduler_cores']
c.KubeClusterConfig.scheduler_cores_limit = config['cluster']['scheduler_cores_limit']
c.KubeClusterConfig.scheduler_memory = config['cluster']['scheduler_memory']
c.KubeClusterConfig.scheduler_memory_limit = config['cluster']['scheduler_memory_limit']
c.KubeClusterConfig.scheduler_extra_container_config = config['cluster']['scheduler_extra_container_config']
c.KubeClusterConfig.scheduler_extra_pod_config = config['cluster']['scheduler_extra_pod_config']
c.KubeClusterConfig.worker_cores = config['cluster']['worker_cores']
c.KubeClusterConfig.worker_cores_limit = config['cluster']['worker_cores_limit']
c.KubeClusterConfig.worker_memory = config['cluster']['worker_memory']
c.KubeClusterConfig.worker_memory_limit = config['cluster']['worker_memory_limit']
c.KubeClusterConfig.worker_extra_container_config = config['cluster']['worker_extra_container_config']
c.KubeClusterConfig.worker_extra_pod_config = config['cluster']['worker_extra_pod_config']

class NebariAuthentication(JupyterHubAuthenticator):

    async def authenticate(self, request):
        user = await super().authenticate(request)
        url = f'{self.jupyterhub_api_url}/users/{user.name}'
        kwargs = {'headers': {'Authorization': 'token %s' % self.jupyterhub_api_token}, 'ssl': self.ssl_context}
        resp = await self.session.get(url, **kwargs)
        data = (await resp.json())['auth_state']['oauth_user']
        if 'dask_gateway_developer' not in data['roles'] and 'dask_gateway_admin' not in data['roles']:
            raise web.HTTPInternalServerError(reason='Permission failure user does not have required dask_gateway roles')
        user.admin = 'dask_gateway_admin' in data['roles']
        user.groups = [os.path.basename(group) for group in data['groups']]
        return user
c.DaskGateway.authenticator_class = NebariAuthentication
c.JupyterHubAuthenticator.jupyterhub_api_url = config['jupyterhub_api_url']
c.JupyterHubAuthenticator.jupyterhub_api_token = config['jupyterhub_api_token']

def get_packages(conda_prefix):
    try:
        packages = set()
        for filename in os.listdir(os.path.join(conda_prefix, 'conda-meta')):
            if filename.endswith('.json'):
                with open(os.path.join(conda_prefix, 'conda-meta', filename)) as f:
                    packages.add(json.load(f).get('name'))
        return packages
    except OSError as e:
        import logging
        logger = logging.getLogger()
        logger.error(f'An issue with a conda environment was encountered.\n{e}')

def get_conda_prefixes(conda_store_mount):
    for namespace in os.listdir(conda_store_mount):
        if os.path.isdir(os.path.join(conda_store_mount, namespace, 'envs')):
            for name in os.listdir(os.path.join(conda_store_mount, namespace, 'envs')):
                yield (namespace, name, os.path.join(conda_store_mount, namespace, 'envs', name))

def list_dask_environments(conda_store_mount):
    for namespace, name, conda_prefix in get_conda_prefixes(conda_store_mount):
        packages = get_packages(conda_prefix)
        if packages and {'dask', 'distributed'} <= packages:
            yield (namespace, name, conda_prefix)

def base_node_group(options):
    default_node_group = {config['worker-node-group']['key']: config['worker-node-group']['value']}
    worker_node_group = config['profiles'][options.profile].get('worker_extra_pod_config', {}).get('nodeSelector')
    worker_node_group = default_node_group if worker_node_group is None else worker_node_group
    scheduler_node_group = config['profiles'][options.profile].get('scheduler_extra_pod_config', {}).get('nodeSelector')
    scheduler_node_group = default_node_group if scheduler_node_group is None else scheduler_node_group
    return {'scheduler_extra_pod_config': {'nodeSelector': scheduler_node_group}, 'worker_extra_pod_config': {'nodeSelector': worker_node_group}}

def base_conda_store_mounts(namespace, name):
    conda_store_pvc_name = config['conda-store-pvc']
    conda_store_mount = config['conda-store-mount']
    return {'scheduler_extra_pod_config': {'volumes': [{'name': 'conda-store', 'persistentVolumeClaim': {'claimName': conda_store_pvc_name}}]}, 'scheduler_extra_container_config': {'volumeMounts': [{'mountPath': os.path.join(conda_store_mount, namespace), 'name': 'conda-store', 'subPath': namespace}]}, 'worker_extra_pod_config': {'volumes': [{'name': 'conda-store', 'persistentVolumeClaim': {'claimName': conda_store_pvc_name}}]}, 'worker_extra_container_config': {'volumeMounts': [{'mountPath': os.path.join(conda_store_mount, namespace), 'name': 'conda-store', 'subPath': namespace}]}, 'worker_cmd': '/opt/conda-run-worker', 'scheduler_cmd': '/opt/conda-run-scheduler', 'environment': {'CONDA_ENVIRONMENT': os.path.join(conda_store_mount, namespace, 'envs', name)}}

def base_username_mount(username, uid=1000, gid=100):
    return {'scheduler_extra_pod_config': {'volumes': [{'name': 'home', 'emptyDir': {}}]}, 'scheduler_extra_container_config': {'securityContext': {'runAsUser': uid, 'runAsGroup': gid, 'fsGroup': gid}, 'workingDir': f'/home/{username}', 'volumeMounts': [{'mountPath': f'/home/{username}', 'name': 'home'}]}, 'worker_extra_pod_config': {'volumes': [{'name': 'home', 'emptyDir': {}}]}, 'worker_extra_container_config': {'securityContext': {'runAsUser': uid, 'runAsGroup': gid, 'fsGroup': gid}, 'workingDir': f'/home/{username}', 'volumeMounts': [{'mountPath': f'/home/{username}', 'name': 'home'}]}, 'environment': {'HOME': f'/home/{username}'}}

def worker_profile(options, user):
    namespace, name = options.conda_environment.split('/')
    return functools.reduce(deep_merge, [base_node_group(options), base_conda_store_mounts(namespace, name), base_username_mount(user.name), config['profiles'][options.profile], {'environment': {**options.environment_vars}}], {})

def user_options(user):
    default_namespace = config['default-conda-store-namespace']
    allowed_namespaces = set([default_namespace, 'global', user.name] + list(user.groups))
    environments = {f'{namespace}/{name}': conda_prefix for namespace, name, conda_prefix in list_dask_environments(config['conda-store-mount']) if namespace in allowed_namespaces}
    args = []
    if environments:
        args += [Select('conda_environment', list(environments.keys()), default=list(environments.keys())[0], label='Environment')]
    if config['profiles']:
        args += [Select('profile', list(config['profiles'].keys()), default=list(config['profiles'].keys())[0], label='Cluster Profile')]
    args += [Mapping('environment_vars', {}, label='Environment Variables')]
    return Options(*args, handler=worker_profile)
c.Backend.cluster_options = user_options

def deep_merge(d1, d2):
    """Deep merge two dictionaries.
    >>> value_1 = {
    'a': [1, 2],
    'b': {'c': 1, 'z': [5, 6]},
    'e': {'f': {'g': {}}},
    'm': 1,
    }.

    >>> value_2 = {
        'a': [3, 4],
        'b': {'d': 2, 'z': [7]},
        'e': {'f': {'h': 1}},
        'm': [1],
    }

    >>> print(deep_merge(value_1, value_2))
    {'m': 1, 'e': {'f': {'g': {}, 'h': 1}}, 'b': {'d': 2, 'c': 1, 'z': [5, 6, 7]}, 'a': [1, 2, 3,  4]}
    """
    if isinstance(d1, dict) and isinstance(d2, dict):
        d3 = {}
        for key in d1.keys() | d2.keys():
            if key in d1 and key in d2:
                d3[key] = deep_merge(d1[key], d2[key])
            elif key in d1:
                d3[key] = d1[key]
            elif key in d2:
                d3[key] = d2[key]
        return d3
    elif isinstance(d1, list) and isinstance(d2, list):
        return [*d1, *d2]
    else:
        return d1