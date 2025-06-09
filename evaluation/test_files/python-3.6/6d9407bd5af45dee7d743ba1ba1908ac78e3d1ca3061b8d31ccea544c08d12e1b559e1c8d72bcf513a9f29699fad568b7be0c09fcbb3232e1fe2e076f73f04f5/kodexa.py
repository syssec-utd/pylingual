"""
Provides classes and utilities to allow you to interact with an instance of the Kodexa
platform.
"""
from __future__ import annotations
import errno
import io
import json
import logging
import os
import sys
import time
from json import JSONDecodeError
import requests
import yaml
from addict import Dict
from appdirs import AppDirs
from kodexa.connectors import get_source
from kodexa.connectors.connectors import get_caller_dir, FolderConnector
from kodexa.model import Document, ExtensionPack
from kodexa.model.objects import AssistantDefinition, Action, Taxonomy, ModelRuntime, CredentialDefinition, ExecutionEvent, ContentObject, AssistantEvent, ContentEvent, ScheduledEvent, Project, Execution, ProjectTemplate, Membership, DataForm
from kodexa.pipeline import PipelineContext, Pipeline, PipelineStatistics
from kodexa.platform.client import DocumentStoreEndpoint, KodexaClient
logger = logging.getLogger()
dirs = AppDirs('Kodexa', 'Kodexa')

def get_config():
    """Get the kodexa config object we use when you want to store your PAT locally

    :return: the config as a dict

    Args:

    Returns:

    """
    path = os.path.join(dirs.user_config_dir, '.kodexa.json')
    if os.path.exists(path):
        with open(path, 'r') as outfile:
            return json.load(outfile)
    else:
        return {'url': None, 'access_token': None}

def save_config(config_obj):
    """Saves the configuration dictionary for the user

    Args:
      config_obj: return:

    Returns:

    """
    path = os.path.join(dirs.user_config_dir, '.kodexa.json')
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(path, 'w') as outfile:
        json.dump(config_obj, outfile)
DEFAULT_COLUMNS = {'extensionPacks': ['ref', 'name', 'description', 'type', 'status'], 'projects': ['id', 'organization.name', 'name', 'description'], 'assistants': ['ref', 'name', 'description', 'template'], 'executions': ['id', 'startDate', 'endDate', 'status', 'assistant.name', 'documentFamily.path'], 'memberships': ['organization.slug', 'organization.name'], 'stores': ['ref', 'name', 'description', 'storeType', 'storePurpose', 'template'], 'default': ['ref', 'name', 'description', 'type', 'template']}
OBJECT_TYPES = {'extensionPacks': {'name': 'extension pack', 'plural': 'extension packs', 'type': ExtensionPack}, 'pipelines': {'name': 'pipeline', 'plural': 'pipelines', 'type': Pipeline}, 'assistants': {'name': 'assistant', 'plural': 'assistants', 'type': AssistantDefinition}, 'actions': {'name': 'action', 'plural': 'actions', 'type': Action}, 'modelRuntimes': {'name': 'modelRuntime', 'plural': 'modelRuntimes', 'type': ModelRuntime}, 'credentialDefinitions': {'name': 'credential definition', 'plural': 'credential definitions', 'type': CredentialDefinition}, 'dataForms': {'name': 'dataForm', 'plural': 'dataForms', 'type': DataForm}, 'taxonomies': {'name': 'taxonomy', 'plural': 'taxonomies', 'type': Taxonomy}, 'stores': {'name': 'store', 'plural': 'stores'}, 'projects': {'name': 'project', 'plural': 'projects', 'type': Project, 'global': True}, 'projectTemplates': {'name': 'project template', 'plural': 'project templates', 'type': ProjectTemplate}, 'executions': {'name': 'execution', 'plural': 'executions', 'type': Execution, 'global': True, 'sort': 'startDate:desc'}, 'memberships': {'name': 'membership', 'plural': 'memberships', 'type': Membership, 'global': True}}

def resolve_object_type(obj_type):
    """Takes part of an object type (ie. pipeline) and then resolves the object type (pipelines)

    Args:
      obj_type: part of the object type

    Returns:
      The object type dict (if found)

    """
    hits = []
    keys = []
    if not isinstance(obj_type, str):
        obj_type = str(obj_type).lower()
    for target_type in OBJECT_TYPES.keys():
        if obj_type in target_type:
            hits.append(OBJECT_TYPES[target_type])
            keys.append(target_type)
    if len(hits) == 1:
        return (keys[0], hits[0])
    if len(hits) == 0:
        print(f':exclaimation: Unable to find object type {obj_type}')
        sys.exit(1)
    else:
        print(f":exclaimation: To many potential matches for object type ({','.join(keys)}")
        sys.exit(1)

class KodexaPlatform:
    """
    The KodexaPlatform object allows you to work with an instance of the Kodexa platform, allow you to list, view and deploy
    components

    Note it also can be used to get your access token and Kodexa platform URL using:

    * A user config file if available
    * Environment variables (KODEXA_ACCESS_TOKEN and KODEXA_URL)

    """

    @staticmethod
    def get_client():
        from kodexa import KodexaClient
        return KodexaClient(KodexaPlatform.get_url(), KodexaPlatform.get_access_token())

    @staticmethod
    def get_access_token() -> str:
        """
        Returns the access token

        >>> access_token = KodexaPlatform.get_access_token()

        Returns: The access token if it is defined in the user config store, or as an environment variable

        """
        kodexa_config = get_config()
        access_token = os.getenv('KODEXA_ACCESS_TOKEN')
        return access_token if access_token is not None else kodexa_config['access_token']

    @staticmethod
    def get_url() -> str:
        """
        Returns the URL to use to access a Kodexa Platform

        The URL should be in the form https://my-company.kodexa.ai

        >>> access_token = KodexaPlatform.get_url()

        Returns: The URL if it is defined in the user config store, or as an environment variable

        """
        kodexa_config = get_config()
        env_url = os.getenv('KODEXA_URL', None)
        return env_url if env_url is not None else kodexa_config['url']

    @staticmethod
    def set_access_token(access_token: str):
        """
        Set to override the access token to use, not that this does not impact your user config stored
        value

        Args:
          access_token:str: The new access token

        Returns: None

        """
        if access_token is not None:
            os.environ['KODEXA_ACCESS_TOKEN'] = access_token

    @staticmethod
    def set_url(url: str):
        """
        Set to override the URL to use, not that this does not impact your user config stored
        value

        Args:
          url:str: The new URL

        Returns: None

        """
        if url is not None:
            os.environ['KODEXA_URL'] = url

    @staticmethod
    def get_access_token_details() -> Dict:
        """
        Pull the access token details (including a list of the available organizations)

        Returns: Dict: details of the access token

        """
        response = requests.get(f'{KodexaPlatform.get_url()}/api/account/accessToken', headers={'x-access-token': KodexaPlatform.get_access_token()})
        if response.status_code == 200:
            return Dict(response.json())
        if response.status_code == 404:
            raise Exception('Unable to find access token')
        raise Exception('An error occurred connecting to the Kodexa platform')

    @staticmethod
    def resolve_ref(ref: str):
        org_slug = ref.split('/')[0]
        slug = ref.split('/')[1].split(':')[0]
        version = None
        if len(ref.split('/')[1].split(':')) == 2:
            version = ref.split('/')[1].split(':')[1]
        return [org_slug, slug, version]

    @classmethod
    def login(cls, kodexa_url, username, password):
        from requests.auth import HTTPBasicAuth
        obj_response = requests.get(f'{kodexa_url}/api/account/me/token', auth=HTTPBasicAuth(username, password), headers={'content-type': 'application/json'})
        if obj_response.status_code == 200:
            kodexa_config = get_config()
            kodexa_config['url'] = kodexa_url
            kodexa_config['access_token'] = obj_response.text
            save_config(kodexa_config)
            print('Logged in')
        else:
            print(f'Check your URL and password [{obj_response.status_code}]')

    @classmethod
    def get_server_info(cls):
        """ """
        r = requests.get(f'{KodexaPlatform.get_url()}/api', headers={'x-access-token': KodexaPlatform.get_access_token(), 'content-type': 'application/json'})
        if r.status_code == 401:
            raise Exception('Your access token was not authorized')
        if r.status_code == 200:
            return r.json()
        logger.warning(r.text)
        raise Exception('Unable to get server information, check your platform settings')

    @classmethod
    def get_tempdir(cls):
        import tempfile
        return os.getenv('KODEXA_TMP', tempfile.gettempdir())

class RemoteSession:
    """A Session on the Kodexa platform for leveraging pipelines and services"""

    def __init__(self, session_type, slug):
        self.session_type = session_type
        self.slug = slug
        self.cloud_session = None

    def get_action_metadata(self, ref):
        """

        Args:
          ref:

        Returns:

        """
        logger.debug(f'Downloading metadata for action {ref}')
        r = requests.get(f"{KodexaPlatform.get_url()}/api/actions/{ref.replace(':', '/')}", headers={'x-access-token': KodexaPlatform.get_access_token()})
        if r.status_code == 401:
            raise Exception('Your access token was not authorized')
        if r.status_code == 200:
            return r.json()
        logger.warning(r.text)
        raise Exception('Unable to get action metadata, check your reference and platform settings')

    def start(self):
        """ """
        logger.info(f'Creating session {self.slug} ({KodexaPlatform.get_url()})')
        r = requests.post(f'{KodexaPlatform.get_url()}/api/sessions', params={self.session_type: self.slug}, headers={'x-access-token': KodexaPlatform.get_access_token()})
        if r.status_code != 200:
            logger.warning('Unable to create session')
            logger.warning(r.text)
            raise Exception('Unable to create a session, check your URL and access token')
        self.cloud_session = Dict(json.loads(r.text))

    def execution_action(self, document, options, attach_source, context):
        files = {}
        if attach_source:
            logger.debug('Attaching source to call')
            files['file'] = get_source(document)
            files['file_document'] = document.to_kddb()
        else:
            files['document'] = document.to_kddb()
        data = {'options': json.dumps(options), 'document_metadata_json': json.dumps(document.metadata), 'context': json.dumps(context.context)}
        logger.info(f'Executing session {self.cloud_session.id}')
        r = requests.post(f'{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/execute', params={self.session_type: self.slug, 'documentVersion': document.version}, data=data, headers={'x-access-token': KodexaPlatform.get_access_token()}, files=files)
        try:
            if r.status_code == 200:
                execution = Dict(json.loads(r.text))
            else:
                logger.warning('Execution creation failed [' + r.text + '], response ' + str(r.status_code))
                raise Exception('Execution creation failed [' + r.text + '], response ' + str(r.status_code))
        except JSONDecodeError:
            logger.warning('Unable to handle response [' + r.text + '], response ' + str(r.status_code))
            raise
        return execution

    def wait_for_execution(self, execution):
        status = execution.status
        while execution.status == 'PENDING' or execution.status == 'RUNNING':
            r = requests.get(f'{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/executions/{execution.id}', headers={'x-access-token': KodexaPlatform.get_access_token()})
            try:
                execution = Dict(json.loads(r.text))
            except JSONDecodeError:
                logger.warning('Unable to handle response [' + r.text + ']')
                raise
            if status != execution.status:
                logger.info(f'Status changed from {status} -> {execution.status}')
                status = execution.status
            time.sleep(5)
        if status == 'FAILED':
            logger.warning('Execution has failed')
            for step in execution.steps:
                if step.status == 'FAILED':
                    logger.warning(f'Step {step.name} has failed. {step.exceptionDetails.message}.')
                    if step.exceptionDetails.errorType == 'Validation':
                        logger.warning('Additional validation information has been provided:')
                        for validation_error in step.exceptionDetails.validationErrors:
                            logger.warning(f'- {validation_error.option} : {validation_error.message}')
                    if step.exceptionDetails.help:
                        logger.warning(f'Additional help is available:\n\n{step.exceptionDetails.help}')
                    raise Exception(f'Processing has failed on step {step.name}')
            raise Exception('Processing has failed, no steps seem to have failed')
        return execution

    def get_output_document(self, execution):
        """
        Get the output document from a given execution

        Args:
          execution: the execution holding the document

        Returns:
            the output document (or None if there isn't one)

        """
        if execution.outputId:
            logger.info(f'Downloading output document [{execution.outputId}]')
            doc = requests.get(f'{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/executions/{execution.id}/objects/{execution.outputId}', headers={'x-access-token': KodexaPlatform.get_access_token()})
            return Document.from_kddb(doc.content)
        logger.info('No output document')
        return None

class RemotePipeline:
    """Allow you to interact with a pipeline that has been deployed to an instance of Kodexa Platform"""

    def __init__(self, slug, connector, version=None, attach_source=True, parameters=None, auth=None):
        logger.info(f'Initializing a new pipeline {slug}')
        if isinstance(connector, Document):
            self.connector = [connector]
        else:
            self.connector = connector
        self.context: PipelineContext = PipelineContext()
        if auth is None:
            auth = []
        if parameters is None:
            parameters = {}
        self.slug = slug
        self.version = version
        self.attach_source = attach_source
        self.parameters = parameters
        self.auth = auth

    def run(self):
        """ """
        self.context.statistics = PipelineStatistics()
        logger.info(f'Starting remote pipeline {self.slug}')
        cloud_session = RemoteSession('pipeline', self.slug)
        cloud_session.start()
        for document in self.connector:
            logger.info(f'Processing {document}')
            execution = cloud_session.execution_action(document, self.parameters, self.attach_source, self.context)
            execution = cloud_session.wait_for_execution(execution)
            logger.info('Capturing output')
            result_document = cloud_session.get_output_document(execution)
            self.context.set_output_document(result_document)
            self.context.statistics.processed_document(result_document)
            self.context.context = execution.context
        logger.info(f'Completed pipeline {self.slug}')
        return self.context

    @staticmethod
    def from_url(slug: str, url, headers=None, *args, **kwargs) -> RemotePipeline:
        """Build a new pipeline with the input being a document created from the given URL

        Args:
          slug: The slug for the remote pipeline
          url: The URL ie. https://www.google.com
          headers: A dictionary of headers (Default value = None)
          slug: str:
          *args:
          **kwargs:

        Returns:
          A new instance of a remote pipeline

        """
        return RemotePipeline(slug, Document.from_url(url, headers), *args, **kwargs)

    @staticmethod
    def from_file(slug: str, file_path: str, unpack: bool=False, *args, **kwargs) -> RemotePipeline:
        """Create a new pipeline using a file path as a source

        Args:
          slug: The slug for the remote pipeline
          file_path: The path to the file
          unpack: Unpack the file as a KDXA
          slug: str:
          file_path: str:
          unpack: bool:  (Default value = False)
          *args:
          **kwargs:

        Returns:
          Pipeline: A new pipeline

        """
        return RemotePipeline(slug, Document.from_file(file_path, unpack), *args, **kwargs)

    @staticmethod
    def from_text(slug: str, text: str, *args, **kwargs) -> RemotePipeline:
        """Build a new pipeline and provide text as the basic to create a document

        Args:
          slug: The slug for the remote pipeline
          text: Text to use to create document
          slug: str:
          text: str:
          *args:
          **kwargs:

        Returns:
          RemotePipeline: A new pipeline

        """
        kwargs.setdefault('attach_source', False)
        return RemotePipeline(slug, Document.from_text(text), *args, **kwargs)

    @staticmethod
    def from_folder(slug: str, folder_path: str, filename_filter: str='*', recursive: bool=False, unpack: bool=False, relative: bool=False, caller_path: str=get_caller_dir()) -> RemotePipeline:
        """Create a pipeline that will run against a set of local files from a folder

        Args:
          slug: The slug for the remote pipeline
          folder_path: The folder path
          filename_filter: The filter for filename (i.e. *.pdf)
          recursive: Should we look recursively in sub-directories (default False)
          relative: Is the folder path relative to the caller (default False)
          caller_path: The caller path (defaults to trying to work this out from the stack)
          unpack: Unpack the file as a KDXA document
          slug: str:
          folder_path: str:
          filename_filter: str:  (Default value = "*")
          recursive: bool:  (Default value = False)
          unpack: bool:  (Default value = False)
          relative: bool:  (Default value = False)
          caller_path: str:  (Default value = get_caller_dir())

        Returns:
          RemotePipeline: A new pipeline

        """
        return RemotePipeline(slug, FolderConnector(folder_path, filename_filter, recursive, relative, caller_path, unpack=unpack))

class RemoteStep:
    """Allows you to interact with a step that has been deployed in the Kodexa platform"""

    def __init__(self, ref, step_type='ACTION', attach_source=False, options=None):
        if options is None:
            options = {}
        self.ref = ref
        self.step_type = step_type
        self.attach_source = attach_source
        self.options = options

    def to_dict(self):
        """ """
        return {'ref': self.ref, 'step_type': self.step_type, 'options': self.options}

    def get_name(self):
        """ """
        return f'Remote Action ({self.ref})'

    def process(self, document, context):
        cloud_session = RemoteSession('service', self.ref)
        cloud_session.start()
        logger.info(f'Loading metadata for {self.ref}')
        action_metadata = cloud_session.get_action_metadata(self.ref)
        requires_source = False
        if 'requiresSource' in action_metadata['metadata']:
            requires_source = action_metadata['metadata']['requiresSource']
        execution = cloud_session.execution_action(document, self.options, self.attach_source if self.attach_source else requires_source, context)
        logger.debug('Waiting for remote execution')
        execution = cloud_session.wait_for_execution(execution)
        logger.debug('Downloading the result document')
        result_document = cloud_session.get_output_document(execution)
        logger.debug('Set the context to match the context from the execution')
        context.context = execution.context
        return result_document if result_document else document

    def to_configuration(self):
        """Returns a dictionary representing the configuration information for the step

        :return: dictionary representing the configuration of the step

        Args:

        Returns:

        """
        return {'ref': self.ref, 'options': self.options}

class ExtensionHelper:
    """ """

    @staticmethod
    def load_metadata(path) -> dict:
        if os.path.exists(os.path.join(path, 'dharma.json')):
            dharma_metadata_file = open(os.path.join(path, 'dharma.json'))
            dharma_metadata = json.loads(dharma_metadata_file.read())
        elif os.path.exists(os.path.join(path, 'dharma.yml')):
            dharma_metadata_file = open(os.path.join(path, 'dharma.yml'))
            dharma_metadata = yaml.safe_load(dharma_metadata_file.read())
        elif os.path.exists(os.path.join(path, 'kodexa.yml')):
            dharma_metadata_file = open(os.path.join(path, 'kodexa.yml'))
            dharma_metadata = yaml.safe_load(dharma_metadata_file.read())
        else:
            raise Exception('Unable to find a kodexa.yml file describing your extension')
        return dharma_metadata

class EventHelper:

    def __init__(self, event: ExecutionEvent):
        self.event: ExecutionEvent = event

    @staticmethod
    def get_base_event(event_dict: Dict):
        if event_dict['type'] == 'assistant':
            return AssistantEvent(**event_dict)
        if event_dict['type'] == 'content':
            return ContentEvent(**event_dict)
        if event_dict['type'] == 'scheduled':
            return ScheduledEvent(**event_dict)
        raise f'Unknown event type {event_dict}'

    def log(self, message: str):
        response = requests.post(f'{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/logs', json=[{'entry': message}], headers={'x-access-token': KodexaPlatform.get_access_token()}, timeout=300)
        if response.status_code != 200:
            print(f'Logging failed {response.status_code}', flush=True)

    def get_content_object(self, content_object_id: str):
        logger.info(f'Getting content object {content_object_id} in event {self.event.id} in execution {self.event.execution.id}')
        co_response = requests.get(f'{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/objects/{content_object_id}', headers={'x-access-token': KodexaPlatform.get_access_token()}, timeout=300)
        if co_response.status_code != 200:
            logger.error(f'Response {co_response.status_code} {co_response.text}')
            raise Exception(f'Unable to find content object {content_object_id} in execution {self.event.execution.id}')
        return io.BytesIO(co_response.content)

    def put_content_object(self, content_object: ContentObject, content) -> ContentObject:
        files = {'content': content}
        data = {'contentObjectJson': json.dumps(content_object.dict(by_alias=True))}
        logger.info('Posting back content object to execution object')
        co_response = requests.post(f'{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/objects', data=data, headers={'x-access-token': KodexaPlatform.get_access_token()}, files=files, timeout=300)
        if co_response.status_code != 200:
            logger.info('Unable to post back object')
            logger.error(co_response.text)
            raise Exception('Unable to post back content object')
        logger.info('Object posted back')
        return ContentObject.parse_obj(co_response.json())

    def build_pipeline_context(self) -> PipelineContext:
        context = PipelineContext(context={}, content_provider=self, execution_id=self.event.execution.id)
        if self.event.store_ref and self.event.document_family_id:
            logger.info('We have storeRef and document family')
            rds: DocumentStoreEndpoint = KodexaClient().get_object_by_ref('store', self.event.store_ref)
            document_family = rds.get_family(self.event.document_family_id)
            context.document_family = document_family
            context.document_store = rds
        return context

    def get_input_document(self, context):
        for content_object in self.event.execution.content_objects:
            if content_object.id == self.event.input_id:
                input_document_bytes = self.get_content_object(self.event.input_id)
                logger.info('Loading KDDB document')
                input_document = Document.from_kddb(input_document_bytes.read())
                logger.info('Loaded KDDB document')
                context.content_object = content_object
                input_document.uuid = context.content_object.id
                if content_object.store_ref is not None:
                    context.document_store = KodexaClient().get_object_by_ref('store', content_object.store_ref)
                return input_document

class SessionConnector:
    event_helper = None

    @classmethod
    def get_name(cls):
        return 'cloud-content'

    @classmethod
    def get_source(cls, document):
        if cls.event_helper is None:
            raise Exception('The event_helper needs to be set to use this connector')
        logger.info(f'Getting content object {document.source.original_path}')
        return cls.event_helper.get_content_object(document.source.original_path)