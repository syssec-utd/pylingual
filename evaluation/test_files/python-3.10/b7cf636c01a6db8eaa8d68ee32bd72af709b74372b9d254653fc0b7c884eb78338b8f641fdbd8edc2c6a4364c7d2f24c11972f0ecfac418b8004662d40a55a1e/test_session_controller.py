from datetime import datetime, timezone
import json
import tempfile
from typing import Iterator, Optional, Tuple
from unittest.mock import ANY, call, MagicMock, Mock, mock_open, patch
import click
import pytest
import yaml
from anyscale.client.openapi_client import AppConfig, Build, Cloud, ClusterConfig, ComputeTemplateConfig, CreateComputeTemplate, Project, ProjectDefaultSessionName, ProjectdefaultsessionnameResponse, ProjectListResponse, Session, SessionListResponse, SessionResponse, SessionUpOptions, SetupInitializeSessionOptions, StartEmptySessionResponse, StartemptysessionresponseResponse, StopSessionOptions
from anyscale.controllers.session_controller import SessionController
from anyscale.sdk.anyscale_client import CreateSession, StartSessionOptions, UpdateSession
from anyscale.shared_anyscale_utils.project import CLUSTER_YAML_TEMPLATE
COMPUTE_CONFIG_TEMPLATE = json.dumps({'cloud_id': 'fake-cloud-id', 'region': 'fake-region', 'allowed_azs': ['fake-az1'], 'head_node_type': {'name': 'head-node-name', 'instance_type': 'fake-head-instance-type'}, 'worker_node_types': [{'name': 'worker-node-name', 'instance_type': 'fake-worker-instance-type', 'min_workers': 0, 'max_workers': 10, 'use_spot': True}], 'aws': {'SubnetId': 'fake-subnet-id', 'SecurityGroupIds': ['fake-security-group-id'], 'IamInstanceProfile': 'fake-iam-arn', 'TagSpecifications': [{'ResourceType': 'instance', 'Tags': [{'Key': 'fake-key', 'Value': 'fake-value'}]}]}})

@pytest.fixture()
def mock_auth_api_client(mock_api_client: Mock, base_mock_anyscale_api_client: Mock):
    mock_auth_api_client = Mock(api_client=mock_api_client, anyscale_api_client=base_mock_anyscale_api_client)
    with patch.multiple('anyscale.controllers.base_controller', get_auth_api_client=Mock(return_value=mock_auth_api_client)):
        yield

@pytest.fixture()
def mock_auth_api_client_multiple_sessions(mock_api_client_multiple_sessions: Mock, base_mock_anyscale_api_client: Mock):
    mock_auth_api_client = Mock(api_client=mock_api_client_multiple_sessions, anyscale_api_client=base_mock_anyscale_api_client)
    with patch.multiple('anyscale.controllers.base_controller', get_auth_api_client=Mock(return_value=mock_auth_api_client)):
        yield

@pytest.fixture()
def mock_auth_api_client_with_session(mock_api_client_with_session: Mock, base_mock_anyscale_api_client: Mock):
    mock_auth_api_client = Mock(api_client=mock_api_client_with_session, anyscale_api_client=base_mock_anyscale_api_client)
    with patch.multiple('anyscale.controllers.base_controller', get_auth_api_client=Mock(return_value=mock_auth_api_client)):
        yield

@pytest.fixture()
def mock_api_client(mock_api_client_with_session: Mock) -> Mock:
    mock_api_client = mock_api_client_with_session
    mock_api_client.stop_session_api_v2_sessions_session_id_stop_post.return_value = None
    return mock_api_client

def test_stop_single_session(session_test_data: Session, mock_auth_api_client) -> None:
    session_controller = SessionController()
    mock_project_definition = Mock()
    mock_project_definition.root = '/some/directory'
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)
    mock_get_project_id = Mock(return_value=session_test_data.project_id)
    with patch.multiple('anyscale.controllers.session_controller', load_project_or_throw=mock_load_project_or_throw, get_project_id=mock_get_project_id):
        session_controller.stop('test-name', delete=False, workers_only=False, keep_min_workers=False)
    session_controller.api_client.stop_session_api_v2_sessions_session_id_stop_post.assert_called_once_with(session_test_data.id, StopSessionOptions(terminate=True, delete=False, workers_only=False, keep_min_workers=False))
    mock_load_project_or_throw.assert_called_once_with()
    mock_get_project_id.assert_called_once_with('/some/directory')

@pytest.fixture()
def mock_api_client_multiple_sessions(base_mock_api_client: Mock) -> Mock:
    base_mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(results=[Session(id='ses_1', name='session_name', created_at=datetime.now(tz=timezone.utc), snapshots_history=[], tensorboard_available=False, project_id='project_id', state='Running', head_node_ip='127.0.0.1', idle_timeout=120, access_token='value'), Session(id='ses_2', name='session_name2', created_at=datetime.now(tz=timezone.utc), snapshots_history=[], tensorboard_available=False, project_id='project_id', state='Running', head_node_ip='127.0.0.1', idle_timeout=120, access_token='value')])
    base_mock_api_client.stop_session_api_v2_sessions_session_id_stop_post.return_value = None
    base_mock_api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get.return_value.result.head_ip = '127.0.0.1'
    return base_mock_api_client

def test_stop_multiple_sessions(mock_auth_api_client_multiple_sessions) -> None:
    session_controller = SessionController()
    mock_project_definition = Mock()
    mock_project_definition.root = '/some/directory'
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)
    mock_get_project_id = Mock(return_value='project_id')
    with patch.multiple('anyscale.controllers.session_controller', load_project_or_throw=mock_load_project_or_throw, get_project_id=mock_get_project_id):
        session_controller.stop('ses_?', delete=True, workers_only=True, keep_min_workers=True)
    session_controller.api_client.stop_session_api_v2_sessions_session_id_stop_post.assert_has_calls([call('ses_1', StopSessionOptions(terminate=True, delete=True, workers_only=True, keep_min_workers=True)), call('ses_2', StopSessionOptions(terminate=True, delete=True, workers_only=True, keep_min_workers=True))])
    mock_load_project_or_throw.assert_called_once_with()
    mock_get_project_id.assert_called_once_with('/some/directory')

@pytest.fixture()
def mock_up_tuple(base_mock_api_client: Mock, project_test_data: Project, cloud_test_data: Cloud, session_test_data: Session) -> Iterator[Tuple[Mock, Project, Cloud, Mock]]:
    base_mock_api_client.get_session_api_v2_sessions_session_id_get = Mock(return_value=SessionResponse(result=session_test_data))
    mock_project_definition = Mock()
    mock_project_definition.root = '/some/directory'
    mock_wait_for_session_start = Mock()
    with patch.multiple('anyscale.controllers.session_controller', load_project_or_throw=Mock(return_value=mock_project_definition), get_project_id=Mock(return_value=project_test_data.id), get_cloud_id_and_name=Mock(return_value=tuple([cloud_test_data.id, cloud_test_data.name])), wait_for_session_start=mock_wait_for_session_start, wait_for_head_node_start=mock_wait_for_session_start, _update_file_mounts=MagicMock(side_effect=lambda cluster_config, project_root_dir, api_client: cluster_config), get_working_dir=Mock(return_value='mock_working_dir')):
        yield (base_mock_api_client, project_test_data, cloud_test_data, mock_wait_for_session_start)

def test_anyscale_up_success(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client) -> None:
    (mock_api_client, project_test_data, cloud_test_data, _) = mock_up_tuple
    session_controller = SessionController()
    session_controller.push = Mock()
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(result=ProjectDefaultSessionName(name='session-11'))
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(results=[])
    mock_api_client.start_empty_session_api_v2_sessions_start_empty_session_post = Mock(return_value=StartemptysessionresponseResponse(result=StartEmptySessionResponse(session_id='session-10', second_update_required=False)))
    with tempfile.NamedTemporaryFile(mode='w') as temp_file:
        temp_file.write(CLUSTER_YAML_TEMPLATE)
        temp_file.flush()
        session_controller.up(session_name=None, config=temp_file.name, build_id=None, min_workers=None, max_workers=None, no_restart=False, restart_only=False, disable_sync=False, cloud_id=None, cloud_name=None, idle_timeout=-1, compute_config=None)
        mock_api_client.start_empty_session_api_v2_sessions_start_empty_session_post.assert_called_once_with(session_up_options=SessionUpOptions(project_id=project_test_data.id, name='session-11', cluster_config={'config': json.dumps(yaml.safe_load(CLUSTER_YAML_TEMPLATE))}, cloud_id=cloud_test_data.id, idle_timeout=-1, start_empty_head_node_only=True))
        mock_api_client.setup_and_initialize_session_api_v2_sessions_session_id_setup_and_initialize_session_post.assert_called_once_with(session_id='session-10', setup_initialize_session_options=SetupInitializeSessionOptions(project_id=project_test_data.id, cluster_config={'config': json.dumps(yaml.safe_load(CLUSTER_YAML_TEMPLATE))}, restart_only=False, no_restart=False, no_update=True))

def test_anyscale_up_failure(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client) -> None:
    (mock_api_client, _, _, mock_wait_for_start) = mock_up_tuple
    session_controller = SessionController()
    session_controller.push = Mock()
    sesion_id = 'session-10'
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(result=ProjectDefaultSessionName(name='session-11'))
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(results=[])
    mock_api_client.start_empty_session_api_v2_sessions_start_empty_session_post = Mock(return_value=StartemptysessionresponseResponse(result=StartEmptySessionResponse(session_id=sesion_id, second_update_required=False)))
    mock_wait_for_start.side_effect = click.ClickException('Node Failed to Start!')
    with tempfile.NamedTemporaryFile(mode='w') as temp_file:
        temp_file.write(CLUSTER_YAML_TEMPLATE)
        temp_file.flush()
        with pytest.raises(click.ClickException):
            session_controller.up(session_name=None, config=temp_file.name, build_id=None, min_workers=None, max_workers=None, no_restart=False, restart_only=False, disable_sync=False, cloud_id=None, cloud_name=None, idle_timeout=-1, compute_config=None)

def test_anyscale_up_no_config_provided(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client) -> None:
    (mock_api_client, project_test_data, cloud_test_data, _) = mock_up_tuple
    session_controller = SessionController()
    session_controller.push = Mock()
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(result=ProjectDefaultSessionName(name='session-11'))
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(results=[Session])
    mock_api_client.start_empty_session_api_v2_sessions_start_empty_session_post = Mock(return_value=StartemptysessionresponseResponse(result=StartEmptySessionResponse(session_id='session-10', second_update_required=False)))
    mock_api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get.return_value = Mock(result=ClusterConfig(config=CLUSTER_YAML_TEMPLATE, config_with_defaults=CLUSTER_YAML_TEMPLATE))
    session_controller.up(session_name=None, config=None, build_id=None, min_workers=None, max_workers=None, no_restart=False, restart_only=False, disable_sync=False, cloud_id=None, cloud_name=None, idle_timeout=-1, compute_config=None)
    mock_api_client.start_empty_session_api_v2_sessions_start_empty_session_post.assert_called_once_with(session_up_options=SessionUpOptions(project_id=project_test_data.id, name='session-11', cluster_config={'config': json.dumps(yaml.safe_load(CLUSTER_YAML_TEMPLATE))}, cloud_id=cloud_test_data.id, idle_timeout=-1, start_empty_head_node_only=True))
    mock_api_client.setup_and_initialize_session_api_v2_sessions_session_id_setup_and_initialize_session_post.assert_called_once_with(session_id='session-10', setup_initialize_session_options=SetupInitializeSessionOptions(project_id=project_test_data.id, cluster_config={'config': json.dumps(yaml.safe_load(CLUSTER_YAML_TEMPLATE))}, restart_only=False, no_restart=False, no_update=True))

def test_anyscale_app_template(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client) -> None:
    (mock_api_client, project_test_data, cloud_test_data, _) = mock_up_tuple
    session_controller = SessionController()
    session_controller.push = Mock()
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(result=ProjectDefaultSessionName(name='session-11'))
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(results=[])
    mock_api_client.start_empty_session_api_v2_sessions_start_empty_session_post = Mock(return_value=StartemptysessionresponseResponse(result=StartEmptySessionResponse(session_id='session-10', second_update_required=False)))
    mock_api_client.create_compute_template_api_v2_compute_templates_post = Mock(return_value=Mock(result=Mock(id='mock_compute_template_id')))
    with tempfile.NamedTemporaryFile(mode='w') as temp_file:
        temp_file.write(COMPUTE_CONFIG_TEMPLATE)
        temp_file.flush()
        session_controller.up(session_name=None, config=None, build_id='mock_build_id', min_workers=None, max_workers=None, no_restart=False, restart_only=False, disable_sync=False, cloud_id=None, cloud_name=None, idle_timeout=-1, compute_config=temp_file.name)
        mock_api_client.start_empty_session_api_v2_sessions_start_empty_session_post.assert_called_once_with(session_up_options=SessionUpOptions(project_id=project_test_data.id, name='session-11', cluster_config=None, build_id='mock_build_id', compute_template_id='mock_compute_template_id', cloud_id=cloud_test_data.id, idle_timeout=-1, start_empty_head_node_only=False))
        mock_api_client.setup_and_initialize_session_api_v2_sessions_session_id_setup_and_initialize_session_post.assert_called_once_with(session_id='session-10', setup_initialize_session_options=SetupInitializeSessionOptions(project_id=project_test_data.id, cluster_config={'config': 'null'}, restart_only=False, no_restart=False, no_update=True))

def test_get_or_generate_session_name(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client) -> None:
    (mock_api_client, project_test_data, _, _) = mock_up_tuple
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(result=ProjectDefaultSessionName(name='session-11'))
    session_controller = SessionController()
    session_controller._get_or_generate_session_name(None, project_test_data.id)
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.assert_called_once_with(project_id=project_test_data.id)

def test_register_compute_config(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client) -> None:
    (mock_api_client, project_test_data, _, _) = mock_up_tuple
    mock_api_client.create_compute_template_api_v2_compute_templates_post = Mock(return_value=Mock(result=Mock(id='mock_compute_template_id')))
    session_controller = SessionController()
    with tempfile.NamedTemporaryFile(mode='w') as temp_file:
        temp_file.write(COMPUTE_CONFIG_TEMPLATE)
        temp_file.flush()
        session_controller._register_compute_config(temp_file.name, project_test_data.id)
    config_object = ComputeTemplateConfig(**yaml.safe_load(COMPUTE_CONFIG_TEMPLATE))
    create_compute_template = CreateComputeTemplate(name=ANY, project_id=project_test_data.id, config=config_object)
    mock_api_client.create_compute_template_api_v2_compute_templates_post.assert_called_once_with(create_compute_template=create_compute_template)

@pytest.mark.parametrize('update_session', [False, True])
def test_create_or_update_session_data(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client, update_session: bool) -> None:
    (mock_api_client, project_test_data, _, _) = mock_up_tuple
    session_controller = SessionController()
    session_controller.api_client = mock_api_client
    if update_session:
        session_controller.api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(results=[Mock(id='session-11-id')])
    else:
        session_controller.api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(results=[])
    session_controller._create_or_update_session_data(session_name='session-11', project_id=project_test_data.id, build_id='mock_build_id', compute_template_id='mock_compute_template_id', idle_timeout=-1)
    if update_session:
        session_controller.anyscale_api_client.update_session.assert_called_once_with('session-11-id', UpdateSession(idle_timeout=-1))
    else:
        create_session_data = CreateSession(name='session-11', project_id=project_test_data.id, cloud_id=None, cluster_config=None, build_id='mock_build_id', compute_template_id='mock_compute_template_id', idle_timeout=-1, uses_app_config=True)
        session_controller.anyscale_api_client.create_session.assert_called_once_with(create_session_data)

def test_list_app_configs(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client) -> None:
    (mock_api_client, project_test_data, _, _) = mock_up_tuple
    session_controller = SessionController()
    session_controller.api_client = mock_api_client
    session_controller.anyscale_api_client.list_app_configs = Mock(return_value=Mock(results=[], metadata=Mock(next_paging_token=None)))
    session_controller._list_app_configs(project_id=project_test_data.id)
    session_controller.anyscale_api_client.list_app_configs.assert_called_once_with(project_id=project_test_data.id, count=50, paging_token=None)

def test_list_builds(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client) -> None:
    (mock_api_client, _, _, _) = mock_up_tuple
    session_controller = SessionController()
    session_controller.api_client = mock_api_client
    session_controller.anyscale_api_client.list_builds = Mock(return_value=Mock(results=[], metadata=Mock(next_paging_token=None)))
    session_controller._list_builds('mock_app_config_id')
    session_controller.anyscale_api_client.list_builds.assert_called_once_with('mock_app_config_id', count=50, paging_token=None)

def test_get_app_config_id_from_name(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client) -> None:
    (mock_api_client, project_test_data, _, _) = mock_up_tuple
    session_controller = SessionController()
    session_controller.api_client = mock_api_client
    session_controller._list_app_configs = Mock(return_value=[AppConfig(name='mock_app_config_name', id='mock_app_config_id', project_id=project_test_data.id, organization_id='org_1', creator_id=ANY, created_at=ANY, last_modified_at=ANY)])
    app_config_id = session_controller._get_app_config_id_from_name('mock_app_config_name', project_test_data.id)
    assert app_config_id == 'mock_app_config_id'
    session_controller._list_app_configs.assert_called_once_with(project_test_data.id)

@pytest.mark.parametrize('build_identifier', ['my_app_config:1', 'my_app_config'])
def test_get_build_id_from_build_identifier(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client, build_identifier: str) -> None:
    (mock_api_client, project_test_data, _, _) = mock_up_tuple
    session_controller = SessionController()
    session_controller.api_client = mock_api_client
    session_controller._get_app_config_id_from_name = Mock(return_value='mock_app_config_id')
    session_controller._list_builds = Mock(return_value=[Build(revision=1, id='mock_build_id_1', application_template_id='mock_app_config_id', config_json=ANY, creator_id=ANY, status=ANY, created_at=ANY, last_modified_at=ANY), Build(revision=2, id='mock_build_id_2', application_template_id='mock_app_config_id', config_json=ANY, creator_id=ANY, status=ANY, created_at=ANY, last_modified_at=ANY)])
    build_id = session_controller._get_build_id_from_build_identifier(build_identifier, project_test_data.id)
    if build_identifier == 'my_app_config':
        assert build_id == 'mock_build_id_2'
    elif build_identifier == 'my_app_config:1':
        assert build_id == 'mock_build_id_1'
    session_controller._get_app_config_id_from_name.assert_called_once_with('my_app_config', project_test_data.id)
    session_controller._list_builds.assert_called_once_with('mock_app_config_id')

@pytest.mark.parametrize('sync_files', [False, True])
@pytest.mark.parametrize('use_build_id', [False, True])
def test_anyscale_start(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock], mock_auth_api_client, sync_files: bool, use_build_id: bool) -> None:
    (mock_api_client, project_test_data, _, _) = mock_up_tuple
    session_controller = SessionController()
    session_controller.api_client = mock_api_client
    session_controller.push = Mock()
    session_controller._get_or_generate_session_name = Mock(return_value='session-11')
    session_controller._register_compute_config = Mock(return_value='mock_compute_template_id')
    session_controller._create_or_update_session_data = Mock(return_value=Mock(id='session-11-id'))
    session_controller._get_build_id_from_build_identifier = Mock(return_value='mock_build_id')
    if sync_files:
        with pytest.raises(click.ClickException):
            session_controller.start(session_name=None, build_id=None, build_identifier='mock_build_identifier', compute_config='mock_compute_config_file', idle_timeout=-1, sync_files=sync_files)
    elif use_build_id:
        session_controller.start(session_name=None, build_id='mock_build_id', build_identifier=None, compute_config='mock_compute_config_file', idle_timeout=-1, sync_files=sync_files)
    else:
        session_controller.start(session_name=None, build_id=None, build_identifier='mock_build_identifier', compute_config='mock_compute_config_file', idle_timeout=-1, sync_files=sync_files)
    if not sync_files:
        session_controller._get_or_generate_session_name.assert_called_once_with(None, project_test_data.id)
        session_controller._register_compute_config.assert_called_once_with('mock_compute_config_file', project_test_data.id)
        session_controller._create_or_update_session_data.assert_called_once_with('session-11', project_test_data.id, 'mock_build_id', 'mock_compute_template_id', -1)
        session_controller.anyscale_api_client.start_session.assert_called_once_with('session-11-id', StartSessionOptions(build_id='mock_build_id', compute_template_id='mock_compute_template_id'))
        if not use_build_id:
            session_controller._get_build_id_from_build_identifier.assert_called_once_with('mock_build_identifier', project_test_data.id)

@pytest.mark.parametrize('force_head_node', [True, False])
@pytest.mark.parametrize('on_head_node', [True, False])
@pytest.mark.parametrize('worker_node_id', [None, '123456'])
@pytest.mark.parametrize('worker_node_ip', [None, '0.0.0.0'])
def test_ssh_session(session_test_data: Session, mock_auth_api_client_multiple_sessions, on_head_node: bool, worker_node_id: Optional[str], worker_node_ip: Optional[str], force_head_node: bool) -> None:
    session_controller = SessionController()
    mock_project_definition = Mock()
    mock_project_definition.root = '/some/directory'
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)
    mock_get_project_id = Mock(return_value=session_test_data.project_id)
    mock_get_project_session = Mock(return_value=session_test_data)
    mock_cluster_config = {'auth': {'ssh_user': 'ubuntu', 'ssh_private_key': ''}, 'docker': {'container_name': 'ray_container'}}
    mock_get_cluster_config = Mock(return_value=mock_cluster_config)
    mock_ray_init = Mock()
    mock_node_manager_address = '111.111.111.111'
    mock_node_data = [{'NodeID': '123456', 'NodeManagerAddress': mock_node_manager_address}]
    mock_ray_nodes = Mock(return_value=mock_node_data)
    mock_exists = Mock(return_value=on_head_node)
    mock_get_and_validate_project_id = Mock()
    with patch.multiple('anyscale.controllers.session_controller', load_project_or_throw=mock_load_project_or_throw, get_project_id=mock_get_project_id, get_cluster_config=mock_get_cluster_config, get_project_session=mock_get_project_session, get_and_validate_project_id=mock_get_and_validate_project_id), patch.multiple('subprocess', run=Mock()), patch('builtins.open', mock_open(read_data=str(mock_cluster_config))), patch.multiple('ray', init=mock_ray_init, nodes=mock_ray_nodes), patch.multiple('os.path', exists=mock_exists):
        if force_head_node and (not on_head_node):
            return
        if force_head_node and worker_node_id is None and (worker_node_ip is None) or (worker_node_id is not None and worker_node_ip is not None):
            with pytest.raises(click.ClickException):
                session_controller.ssh(session_name=session_test_data.name, ssh_option=('',), worker_node_id=worker_node_id, worker_node_ip=worker_node_ip, force_head_node=force_head_node, project_id=None)
            return
        else:
            session_controller.ssh(session_name=session_test_data.name, ssh_option=('',), worker_node_id=worker_node_id, worker_node_ip=worker_node_ip, force_head_node=force_head_node, project_id=None)
    if on_head_node and worker_node_id is not None:
        mock_ray_init.assert_called_once_with(address='auto')
        mock_ray_nodes.assert_called_once_with()
    elif on_head_node and worker_node_ip is not None:
        mock_ray_init.assert_not_called()
        mock_ray_nodes.assert_not_called()
    elif worker_node_id is not None or worker_node_ip is not None:
        session_controller.api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get.assert_called_once_with(session_test_data.id)
    else:
        session_controller.api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get.assert_called_once_with(session_test_data.id)
        mock_get_and_validate_project_id.assert_called_once_with(project_id=None, project_name=None, api_client=session_controller.api_client, anyscale_api_client=session_controller.anyscale_api_client)

def test_anyscale_push_session(session_test_data: Session, mock_auth_api_client_with_session) -> None:
    mock_project_definition = Mock()
    mock_project_definition.root = '/some/directory'
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)
    mock_get_project_id = Mock(return_value=session_test_data.project_id)
    mock_get_project_session = Mock(return_value=session_test_data)
    cluster_config_data = {'auth': {'ssh_user': '', 'ssh_private_key': ''}}
    mock_get_cluster_config = Mock(return_value=cluster_config_data)
    mock_subprocess_run = Mock()
    mock_subprocess_run.return_value.returncode = 0
    mock_validate_cluster_configuration = Mock()
    mock_rsync = Mock()
    mock_up = Mock()
    session_controller = SessionController()
    with patch.multiple('subprocess', run=mock_subprocess_run), patch.multiple('anyscale.controllers.session_controller', load_project_or_throw=mock_load_project_or_throw, get_project_id=mock_get_project_id, get_cluster_config=mock_get_cluster_config, get_project_session=mock_get_project_session, validate_cluster_configuration=mock_validate_cluster_configuration, rsync=mock_rsync), patch.object(session_controller, 'up', new=mock_up):
        session_name = 'TestSessionName'
        source = 'TestSource'
        target = 'TestTarget'
        config = 'TestConfig'
        all_nodes = False
        session_controller.push(session_name, source, target, config, all_nodes)
        mock_rsync.assert_called_once_with(ANY, source=source, target=target, down=False)
        mock_validate_cluster_configuration.assert_called_once_with(config, api_instance=session_controller.api_client)
        mock_up.assert_called_once_with(session_name=session_test_data.name, config=None, build_id=None, compute_config=None, min_workers=None, max_workers=None, no_restart=False, idle_timeout=None, restart_only=False, disable_sync=True, cloud_id=session_test_data.cloud_id, cloud_name=None)

@pytest.mark.parametrize('config', [None, 'tmp.yaml'])
def test_pull(session_test_data: Session, mock_auth_api_client_with_session, config: str) -> None:
    mock_project_definition = Mock()
    mock_project_definition.root = '/some/directory'
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)
    mock_get_project_id = Mock(return_value=session_test_data.project_id)
    cluster_config_data = {'auth': {'ssh_user': '', 'ssh_private_key': ''}}
    mock_get_cluster_config = Mock(return_value=cluster_config_data)
    mock_get_working_dir = Mock(return_value='directory')
    mock_rsync = Mock()
    mock_get_project_session = Mock(return_value=session_test_data)
    session_controller = SessionController()
    session_controller.api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get.return_value.result.config_with_defaults = 'temp'
    with patch.multiple('anyscale.controllers.session_controller', load_project_or_throw=mock_load_project_or_throw, get_project_id=mock_get_project_id, get_cluster_config=mock_get_cluster_config, get_working_dir=mock_get_working_dir, get_project_session=mock_get_project_session, rsync=mock_rsync), patch('builtins.open', new_callable=mock_open()), patch('yaml.dump'):
        session_controller.pull(session_name=session_test_data.name, config=config)
    mock_load_project_or_throw.assert_called_once_with()
    mock_get_project_id.assert_called_once_with('/some/directory')
    mock_get_cluster_config.assert_called_once_with(session_test_data.name, session_controller.api_client)
    mock_get_working_dir.assert_called_once_with(cluster_config_data, session_test_data.project_id, session_controller.api_client)
    mock_rsync.assert_called_once()
    if config:
        mock_get_project_session.assert_called_once_with(session_test_data.project_id, session_test_data.name, session_controller.api_client)
        session_controller.api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get.assert_called_once_with(session_test_data.id)

@pytest.mark.parametrize('project_name', [None, 'project_name'])
def test_resolve_session(project_test_data: Project, session_test_data: Session, mock_auth_api_client_with_session, project_name: Optional[str]) -> None:
    mock_project_definition = Mock()
    mock_project_definition.root = '/some/directory'
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)
    mock_get_project_id = Mock(return_value=session_test_data.project_id)
    session_controller = SessionController()
    session_controller.api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(results=[session_test_data])
    session_controller.api_client.list_projects_api_v2_projects_get.return_value = ProjectListResponse(results=[project_test_data])
    with patch.multiple('anyscale.controllers.session_controller', load_project_or_throw=mock_load_project_or_throw, get_project_id=mock_get_project_id):
        session = session_controller._resolve_session('session_name', project_name)
    assert session == session_test_data
    if project_name:
        mock_load_project_or_throw.assert_not_called()
        mock_get_project_id.assert_not_called()
        session_controller.api_client.list_projects_api_v2_projects_get.assert_called_once_with()
    else:
        mock_load_project_or_throw.assert_called_once()
        mock_get_project_id.assert_called_once_with(mock_project_definition.root)
        session_controller.api_client.list_projects_api_v2_projects_get.assert_not_called()
    session_controller.api_client.list_sessions_api_v2_sessions_get.assert_called_once_with(session_test_data.project_id, name='session_name')