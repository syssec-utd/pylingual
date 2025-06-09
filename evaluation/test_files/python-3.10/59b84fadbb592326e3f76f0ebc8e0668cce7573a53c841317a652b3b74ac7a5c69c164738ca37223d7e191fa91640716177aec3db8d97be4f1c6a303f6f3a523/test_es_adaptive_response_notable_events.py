from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible.module_utils.six import PY2
builtin_import = 'builtins.__import__'
if PY2:
    builtin_import = '__builtin__.__import__'
import tempfile
from ansible.playbook.task import Task
from ansible.template import Templar
from ansible_collections.splunk.es.plugins.action.splunk_adaptive_response_notable_events import ActionModule
from ansible_collections.splunk.es.plugins.module_utils.splunk import SplunkRequest
from ansible_collections.ansible.utils.tests.unit.compat.mock import MagicMock, patch
RESPONSE_PAYLOAD = [{'entry': [{'content': {'action.notable.param.default_owner': '', 'action.notable.param.default_status': '0', 'action.notable.param.drilldown_name': 'test_drill_name', 'action.notable.param.drilldown_search': 'test_drill', 'action.notable.param.drilldown_earliest_offset': '$info_min_time$', 'action.notable.param.drilldown_latest_offset': '$info_max_time$', 'action.notable.param.extract_artifacts': '{"asset": ["src", "dest", "dvc", "orig_host"],"identity": ["src_user", "user", "src_user_id", "src_user_role", "user_id", "user_role", "vendor_account"]}', 'action.notable.param.investigation_profiles': '{"profile://test profile 1":{}, "profile://test profile 2":{}, "profile://test profile 3":{}}', 'action.notable.param.next_steps': '{"version": 1, "data": "[[action|makestreams]][[action|nbtstat]][[action|nslookup]]"}', 'action.notable.param.recommended_actions': 'email,logevent,makestreams,nbtstat', 'action.notable.param.rule_description': 'test notable event', 'action.notable.param.rule_title': 'ansible_test_notable', 'action.notable.param.security_domain': 'threat', 'action.notable.param.severity': 'high', 'search': '| tstats summariesonly=true values("Authentication.tag") as "tag",dc("Authentication.user") as "user_count",dc("Authentication.dest") as "dest_count",count from datamodel="Authentication"."Authentication" where nodename="Authentication.Failed_Authentication" by "Authentication.app","Authentication.src" | rename "Authentication.app" as "app","Authentication.src" as "src" | where "count">=6', 'actions': 'notable'}, 'name': 'Ansible Test'}]}, {'entry': [{'content': {'action.notable.param.default_owner': '', 'action.notable.param.default_status': '', 'action.notable.param.drilldown_name': 'test_drill_name', 'action.notable.param.drilldown_search': 'test_drill', 'action.notable.param.drilldown_earliest_offset': '$info_min_time$', 'action.notable.param.drilldown_latest_offset': '$info_max_time$', 'action.notable.param.extract_artifacts': '{"asset": ["src", "dest"],"identity": ["src_user", "user", "src_user_id"]}', 'action.notable.param.investigation_profiles': '{"profile://test profile 1":{}, "profile://test profile 2":{}, "profile://test profile 3":{}}', 'action.notable.param.next_steps': '{"version": 1, "data": "[[action|makestreams]]"}', 'action.notable.param.recommended_actions': 'email,logevent', 'action.notable.param.rule_description': 'test notable event', 'action.notable.param.rule_title': 'ansible_test_notable', 'action.notable.param.security_domain': 'threat', 'action.notable.param.severity': 'high', 'search': '| tstats summariesonly=true values("Authentication.tag") as "tag",dc("Authentication.user") as "user_count",dc("Authentication.dest") as "dest_count",count from datamodel="Authentication"."Authentication" where nodename="Authentication.Failed_Authentication" by "Authentication.app","Authentication.src" | rename "Authentication.app" as "app","Authentication.src" as "src" | where "count">=6', 'actions': 'notable'}, 'name': 'Ansible Test'}]}]
REQUEST_PAYLOAD = [{'correlation_search_name': 'Ansible Test', 'default_status': 'unassigned', 'description': 'test notable event', 'drilldown_earliest_offset': '$info_min_time$', 'drilldown_latest_offset': '$info_max_time$', 'drilldown_name': 'test_drill_name', 'drilldown_search': 'test_drill', 'extract_artifacts': {'asset': ['src', 'dest', 'dvc', 'orig_host'], 'identity': ['src_user', 'user', 'src_user_id', 'src_user_role', 'user_id', 'user_role', 'vendor_account']}, 'investigation_profiles': ['test profile 1', 'test profile 2', 'test profile 3'], 'next_steps': ['makestreams', 'nbtstat', 'nslookup'], 'name': 'ansible_test_notable', 'recommended_actions': ['email', 'logevent', 'makestreams', 'nbtstat'], 'security_domain': 'threat', 'severity': 'high'}, {'correlation_search_name': 'Ansible Test', 'description': 'test notable event', 'drilldown_earliest_offset': '$info_min_time$', 'drilldown_latest_offset': '$info_max_time$', 'extract_artifacts': {'asset': ['src', 'dest'], 'identity': ['src_user', 'user', 'src_user_id']}, 'next_steps': ['makestreams'], 'name': 'ansible_test_notable', 'recommended_actions': ['email', 'logevent'], 'security_domain': 'threat', 'severity': 'high'}]

class TestSplunkEsAdaptiveResponseNotableEvents:

    def setup(self):
        task = MagicMock(Task)
        task.check_mode = False
        play_context = MagicMock()
        play_context.check_mode = False
        connection = patch('ansible_collections.splunk.es.plugins.module_utils.splunk.Connection')
        connection._socket_path = tempfile.NamedTemporaryFile().name
        fake_loader = {}
        templar = Templar(loader=fake_loader)
        self._plugin = ActionModule(task=task, connection=connection, play_context=play_context, loader=fake_loader, templar=templar, shared_loader_obj=None)
        self._plugin._task.action = 'adaptive_response_notable_events'
        self._plugin._task.async_val = False
        self._task_vars = {}
        self.metadata = {'search': '| tstats summariesonly=true values("Authentication.tag") as "tag",dc("Authentication.user") as "user_count",dc("Authentication.dest") as "dest_count",count from datamodel="Authentication"."Authentication" where nodename="Authentication.Failed_Authentication" by "Authentication.app","Authentication.src" | rename "Authentication.app" as "app","Authentication.src" as "src" | where "count">=6', 'actions': 'notable'}

    @patch('ansible.module_utils.connection.Connection.__rpc__')
    def test_es_adaptive_response_notable_events_merged_01(self, connection, monkeypatch):
        metadata = {'search': '| tstats summariesonly=true values("Authentication.tag") as "tag",dc("Authentication.user") as "user_count",dc("Authentication.dest") as "dest_count",count from datamodel="Authentication"."Authentication" where nodename="Authentication.Failed_Authentication" by "Authentication.app","Authentication.src" | rename "Authentication.app" as "app","Authentication.src" as "src" | where "count">=6', 'actions': ''}
        self._plugin.api_response = RESPONSE_PAYLOAD[0]
        self._plugin.search_for_resource_name = MagicMock()
        self._plugin.search_for_resource_name.return_value = ({}, metadata)

        def create_update(self, rest_path, data=None):
            return RESPONSE_PAYLOAD[0]
        monkeypatch.setattr(SplunkRequest, 'create_update', create_update)
        self._plugin._connection.socket_path = tempfile.NamedTemporaryFile().name
        self._plugin._connection._shell = MagicMock()
        self._plugin._task.args = {'state': 'merged', 'config': [REQUEST_PAYLOAD[0]]}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result['changed'] is True

    @patch('ansible.module_utils.connection.Connection.__rpc__')
    def test_es_adaptive_response_notable_events_merged_02(self, connection, monkeypatch):
        self._plugin.api_response = RESPONSE_PAYLOAD[0]
        self._plugin.search_for_resource_name = MagicMock()
        self._plugin.search_for_resource_name.return_value = (RESPONSE_PAYLOAD[0], self.metadata)

        def create_update(self, rest_path, data=None):
            return RESPONSE_PAYLOAD[1]
        monkeypatch.setattr(SplunkRequest, 'create_update', create_update)
        self._plugin._connection.socket_path = tempfile.NamedTemporaryFile().name
        self._plugin._connection._shell = MagicMock()
        self._plugin._task.args = {'state': 'merged', 'config': [REQUEST_PAYLOAD[1]]}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result['changed'] is True

    @patch('ansible.module_utils.connection.Connection.__rpc__')
    def test_es_adaptive_response_notable_events_merged_idempotent(self, conn, monkeypatch):
        self._plugin._connection.socket_path = tempfile.NamedTemporaryFile().name
        self._plugin._connection._shell = MagicMock()

        def create_update(self, rest_path, data=None):
            return RESPONSE_PAYLOAD[0]

        def get_by_path(self, path):
            return RESPONSE_PAYLOAD[0]
        monkeypatch.setattr(SplunkRequest, 'create_update', create_update)
        monkeypatch.setattr(SplunkRequest, 'get_by_path', get_by_path)
        self._plugin._task.args = {'state': 'merged', 'config': [REQUEST_PAYLOAD[0]]}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result['changed'] is False

    @patch('ansible.module_utils.connection.Connection.__rpc__')
    def test_es_adaptive_response_notable_events_replaced_01(self, conn, monkeypatch):
        self._plugin._connection.socket_path = tempfile.NamedTemporaryFile().name
        self._plugin._connection._shell = MagicMock()
        self._plugin.search_for_resource_name = MagicMock()
        self._plugin.search_for_resource_name.return_value = (RESPONSE_PAYLOAD[0], self.metadata)

        def create_update(self, rest_path, data=None):
            return RESPONSE_PAYLOAD[0]

        def get_by_path(self, path):
            return RESPONSE_PAYLOAD[0]

        def delete_by_path(self, path):
            return {}
        monkeypatch.setattr(SplunkRequest, 'create_update', create_update)
        monkeypatch.setattr(SplunkRequest, 'get_by_path', get_by_path)
        monkeypatch.setattr(SplunkRequest, 'delete_by_path', delete_by_path)
        self._plugin._task.args = {'state': 'replaced', 'config': [REQUEST_PAYLOAD[1]]}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result['changed'] is True

    @patch('ansible.module_utils.connection.Connection.__rpc__')
    def test_es_adaptive_response_notable_events_replaced_02(self, conn, monkeypatch):
        self._plugin._connection.socket_path = tempfile.NamedTemporaryFile().name
        self._plugin._connection._shell = MagicMock()
        self._plugin.search_for_resource_name = MagicMock()
        self._plugin.search_for_resource_name.return_value = (RESPONSE_PAYLOAD[0], self.metadata)

        def create_update(self, rest_path, data=None):
            return RESPONSE_PAYLOAD[0]

        def get_by_path(self, path):
            return RESPONSE_PAYLOAD[0]

        def delete_by_path(self, path):
            return {}
        monkeypatch.setattr(SplunkRequest, 'create_update', create_update)
        monkeypatch.setattr(SplunkRequest, 'get_by_path', get_by_path)
        monkeypatch.setattr(SplunkRequest, 'delete_by_path', delete_by_path)
        self._plugin._task.args = {'state': 'replaced', 'config': [REQUEST_PAYLOAD[1]]}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result['changed'] is True

    @patch('ansible.module_utils.connection.Connection.__rpc__')
    def test_es_adaptive_response_notable_events_replaced_idempotent(self, conn, monkeypatch):
        self._plugin._connection.socket_path = tempfile.NamedTemporaryFile().name
        self._plugin._connection._shell = MagicMock()

        def create_update(self, rest_path, data=None):
            return RESPONSE_PAYLOAD[0]

        def get_by_path(self, path):
            return RESPONSE_PAYLOAD[0]
        monkeypatch.setattr(SplunkRequest, 'create_update', create_update)
        monkeypatch.setattr(SplunkRequest, 'get_by_path', get_by_path)
        self._plugin._task.args = {'state': 'replaced', 'config': [REQUEST_PAYLOAD[0]]}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result['changed'] is False

    @patch('ansible.module_utils.connection.Connection.__rpc__')
    def test_es_adaptive_response_notable_events_deleted(self, conn, monkeypatch):
        self._plugin._connection.socket_path = tempfile.NamedTemporaryFile().name
        self._plugin._connection._shell = MagicMock()
        self._plugin.search_for_resource_name = MagicMock()
        self._plugin.search_for_resource_name.return_value = (RESPONSE_PAYLOAD[0], self.metadata)

        def create_update(self, rest_path, data=None):
            return RESPONSE_PAYLOAD[0]
        monkeypatch.setattr(SplunkRequest, 'create_update', create_update)
        self._plugin._task.args = {'state': 'deleted', 'config': [{'correlation_search_name': 'Ansible Test'}]}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result['changed'] is True

    @patch('ansible.module_utils.connection.Connection.__rpc__')
    def test_es_adaptive_response_notable_events_deleted_idempotent(self, connection):
        self._plugin._connection.socket_path = tempfile.NamedTemporaryFile().name
        self._plugin._connection._shell = MagicMock()
        self._plugin.search_for_resource_name = MagicMock()
        self._plugin.search_for_resource_name.return_value = ({}, {})
        self._plugin._task.args = {'state': 'deleted', 'config': [{'correlation_search_name': 'Ansible Test'}]}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result['changed'] is False

    @patch('ansible.module_utils.connection.Connection.__rpc__')
    def test_es_adaptive_response_notable_events_gathered(self, conn, monkeypatch):
        self._plugin._connection.socket_path = tempfile.NamedTemporaryFile().name
        self._plugin._connection._shell = MagicMock()
        self._plugin.search_for_resource_name = MagicMock()
        self._plugin.search_for_resource_name.return_value = (RESPONSE_PAYLOAD[0], self.metadata)
        self._plugin._task.args = {'state': 'gathered', 'config': [{'correlation_search_name': 'Ansible Test'}]}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result['changed'] is False