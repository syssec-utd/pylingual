import json
import logging
import sys
from typing import Any, Optional, Union
import jinja2
import yaml
from reconcile import openshift_base as ob
from reconcile import queries
from reconcile.status import ExitCodes
from reconcile.utils import gql
from reconcile.utils.defer import defer
from reconcile.utils.openshift_resource import OpenshiftResource as OR
from reconcile.utils.saasherder import Providers
from reconcile.utils.semver_helper import make_semver
from reconcile.utils.sharding import is_in_shard
LOG = logging.getLogger(__name__)
QONTRACT_INTEGRATION = 'openshift-tekton-resources'
QONTRACT_INTEGRATION_VERSION = make_semver(0, 1, 0)
OBJECTS_PREFIX = 'o'
RESOURCE_MAX_LENGTH = 63
DEFAULT_DEPLOY_RESOURCES_STEP_NAME = 'qontract-reconcile'
DEFAULT_DEPLOY_RESOURCES = {'requests': {'cpu': '300m', 'memory': '600Mi'}, 'limits': {'cpu': '300m', 'memory': '600Mi'}}
SAAS_FILES_QUERY = '\n{\n  saas_files: saas_files_v2 {\n    path\n    name\n    pipelinesProvider {\n      name\n      provider\n    }\n    deployResources {\n      requests {\n        cpu\n        memory\n      }\n      limits {\n        cpu\n        memory\n      }\n    }\n  }\n}\n'

class OpenshiftTektonResourcesNameTooLongError(Exception):
    pass

class OpenshiftTektonResourcesBadConfigError(Exception):
    pass

def fetch_saas_files(saas_file_name: Optional[str]) -> list[dict[str, Any]]:
    """Fetch saas v2 files"""
    saas_files = gql.get_api().query(SAAS_FILES_QUERY)['saas_files']
    if saas_file_name:
        saas_file = None
        for sf in saas_files:
            if sf['name'] == saas_file_name:
                saas_file = sf
                break
        return [saas_file] if saas_file else []
    return saas_files

def fetch_tkn_providers(saas_file_name: Optional[str]) -> dict[str, Any]:
    """Fetch tekton providers data for the saas files handled here"""
    saas_files = fetch_saas_files(saas_file_name)
    if not saas_files:
        return {}
    duplicates: set[str] = set()
    all_tkn_providers = {}
    for pipeline_provider in queries.get_pipelines_providers():
        if pipeline_provider['provider'] != Providers.TEKTON:
            continue
        if pipeline_provider['name'] in all_tkn_providers:
            duplicates.add(pipeline_provider['name'])
        else:
            all_tkn_providers[pipeline_provider['name']] = pipeline_provider
    if duplicates:
        raise OpenshiftTektonResourcesBadConfigError(f"There are duplicates in tekton providers names: {', '.join(duplicates)}")
    tkn_providers = {}
    for sf in saas_files:
        provider_name = sf['pipelinesProvider']['name']
        if provider_name not in tkn_providers:
            tkn_providers[provider_name] = all_tkn_providers[provider_name]
        if 'saas_files' not in tkn_providers[provider_name]:
            tkn_providers[provider_name]['saas_files'] = []
        tkn_providers[provider_name]['saas_files'].append(sf)
    return {provider_name: sf for (provider_name, sf) in tkn_providers.items() if is_in_shard(provider_name)}

def fetch_desired_resources(tkn_providers: dict[str, Any]) -> list[dict[str, Union[str, OR]]]:
    """Create an array of dicts that will be used as args of ri.add_desired
    This will also add resourceNames inside tkn_providers['namespace']
    while we are migrating from the current system to this integration"""
    desired_resources = []
    for tknp in tkn_providers.values():
        namespace = tknp['namespace']['name']
        cluster = tknp['namespace']['cluster']['name']
        deploy_resources = tknp.get('deployResources') or DEFAULT_DEPLOY_RESOURCES
        task_templates_types = {}
        desired_tasks = []
        for task_template_config in tknp['taskTemplates']:
            task_templates_types[task_template_config['name']] = task_template_config['type']
            if task_template_config['type'] == 'onePerNamespace':
                task = build_one_per_namespace_task(task_template_config)
                desired_tasks.append(build_desired_resource(task, task_template_config['path'], cluster, namespace))
            elif task_template_config['type'] == 'onePerSaasFile':
                for sf in tknp['saas_files']:
                    task = build_one_per_saas_file_task(task_template_config, sf, deploy_resources)
                    desired_tasks.append(build_desired_resource(task, task_template_config['path'], cluster, namespace))
            else:
                raise OpenshiftTektonResourcesBadConfigError(f"Unknown type [{task_template_config['type']}] in tekton provider [{tknp['name']}]")
        if len(tknp['taskTemplates']) != len(task_templates_types.keys()):
            raise OpenshiftTektonResourcesBadConfigError(f"There are duplicates in task templates names in tekton provider {tknp['name']}")
        desired_resources.extend(desired_tasks)
        pipeline_template_config = tknp['pipelineTemplates']['openshiftSaasDeploy']
        desired_pipelines = []
        for sf in tknp['saas_files']:
            pipeline = build_one_per_saas_file_pipeline(pipeline_template_config, sf, task_templates_types)
            desired_pipelines.append(build_desired_resource(pipeline, pipeline_template_config['path'], cluster, namespace))
        desired_resources.extend(desired_pipelines)
    return desired_resources

def build_one_per_namespace_task(task_template_config: dict[str, str]) -> dict[str, Any]:
    """Builds onePerNamespace Task objects. The name of the task template
    will be used as Task name and there won't be any resource configuration"""
    variables = json.loads(task_template_config['variables']) if task_template_config.get('variables') else {}
    task = load_tkn_template(task_template_config['path'], variables)
    task['metadata']['name'] = build_one_per_namespace_tkn_object_name(task_template_config['name'])
    return task

def build_one_per_saas_file_task(task_template_config: dict[str, str], saas_file: dict[str, Any], deploy_resources: dict[str, dict[str, str]]) -> dict[str, Any]:
    """Builds onePerSaasFile Task objects. The name of the Task will be set
    using the template config name and the saas file name. The step
    corresponding to the openshift-saas-deploy run will get its resources
    configured using either the defaults, the provider defaults or the saas
    file configuration"""
    variables = json.loads(task_template_config['variables']) if task_template_config.get('variables') else {}
    task = load_tkn_template(task_template_config['path'], variables)
    task['metadata']['name'] = build_one_per_saas_file_tkn_object_name(task_template_config['name'], saas_file['name'])
    step_name = task_template_config.get('deployResourcesStepName', DEFAULT_DEPLOY_RESOURCES_STEP_NAME)
    resources_configured = False
    for step in task['spec']['steps']:
        if step['name'] == step_name:
            step['resources'] = saas_file.get('deployResources') or deploy_resources
            resources_configured = True
            break
    if not resources_configured:
        raise OpenshiftTektonResourcesBadConfigError(f"Cannot find a step named {step_name} to set resources in task template {task_template_config['name']}")
    return task

def build_one_per_saas_file_pipeline(pipeline_template_config: dict[str, str], saas_file: dict[str, Any], task_templates_types: dict[str, str]) -> dict[str, Any]:
    """Builds onePerSaasFile Pipeline objects. The task references names will
    be set depending if the tasks are onePerNamespace or onePerSaasFile"""
    variables = json.loads(pipeline_template_config['variables']) if pipeline_template_config.get('variables') else {}
    pipeline = load_tkn_template(pipeline_template_config['path'], variables)
    pipeline['metadata']['name'] = build_one_per_saas_file_tkn_object_name(pipeline_template_config['name'], saas_file['name'])
    for section in ['tasks', 'finally']:
        for task in pipeline['spec'].get(section, []):
            if task['name'] not in task_templates_types:
                raise OpenshiftTektonResourcesBadConfigError(f"Unknown task {task['name']} in pipeline template {pipeline_template_config['name']}")
            if task_templates_types[task['name']] == 'onePerNamespace':
                task['taskRef']['name'] = build_one_per_namespace_tkn_object_name(task['name'])
            else:
                task['taskRef']['name'] = build_one_per_saas_file_tkn_object_name(task['name'], saas_file['name'])
    return pipeline

def load_tkn_template(path: str, variables: dict[str, str]) -> dict[str, Any]:
    """Fetches a yaml resource from qontract-server and parses it"""
    resource = gql.get_api().get_resource(path)
    body = jinja2.Template(resource['content'], undefined=jinja2.StrictUndefined).render(variables)
    return yaml.safe_load(body)

def build_desired_resource(tkn_object: dict[str, Any], path: str, cluster: str, namespace: str) -> dict[str, Union[str, OR]]:
    """Returns a dict with ResourceInventory.add_desired args"""
    openshift_resource = OR(tkn_object, QONTRACT_INTEGRATION, QONTRACT_INTEGRATION_VERSION, error_details=path)
    return {'cluster': cluster, 'namespace': namespace, 'resource_type': openshift_resource.kind, 'name': openshift_resource.name, 'value': openshift_resource}

def check_resource_max_length(name: str) -> None:
    """Checks the resource name is not too long as it may have problems while
    being applied"""
    if len(name) > RESOURCE_MAX_LENGTH:
        raise OpenshiftTektonResourcesNameTooLongError(f'name {name} is longer than {RESOURCE_MAX_LENGTH} characters')

def build_one_per_namespace_tkn_object_name(name: str) -> str:
    """Builds a onePerNamespace object name"""
    name = f'{OBJECTS_PREFIX}-{name}'
    check_resource_max_length(name)
    return name

def build_one_per_saas_file_tkn_object_name(template_name: str, saas_file_name: str) -> str:
    """Builds a onePerSaasFile object name.  Given a saas file name, it returns
    the openshift-saas-deploy names used by Tasks and Pipelines created by this
    integration"""
    name = f'{OBJECTS_PREFIX}-{template_name}-{saas_file_name}'
    check_resource_max_length(name)
    return name

def run(dry_run: bool, thread_pool_size: int=10, internal: Optional[bool]=None, use_jump_host: bool=True, saas_file_name: Optional[str]=None) -> None:
    tkn_providers = fetch_tkn_providers(saas_file_name)
    if not tkn_providers:
        LOG.debug('No saas files found to be processed')
        sys.exit(0)
    LOG.debug('Fetching desired resources')
    desired_resources = fetch_desired_resources(tkn_providers)
    tkn_namespaces = [tknp['namespace'] for tknp in tkn_providers.values()]
    LOG.debug('Fetching current resources')
    (ri, oc_map) = ob.fetch_current_state(namespaces=tkn_namespaces, integration=QONTRACT_INTEGRATION, integration_version=QONTRACT_INTEGRATION_VERSION, override_managed_types=['Pipeline', 'Task'], internal=internal, use_jump_host=use_jump_host, thread_pool_size=thread_pool_size)
    defer(oc_map.cleanup)
    LOG.debug('Adding desired resources to inventory')
    for desired_resource in desired_resources:
        ri.add_desired(**desired_resource)
    LOG.debug('Realizing data')
    ob.realize_data(dry_run, oc_map, ri, thread_pool_size)
    if ri.has_error_registered():
        sys.exit(ExitCodes.ERROR)
    sys.exit(0)