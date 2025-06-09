from taskflow import engines
from taskflow.patterns import linear_flow
from unittest import mock
from magnum.conductor.tasks import heat_tasks
from magnum.tests import base

class HeatTasksTests(base.TestCase):

    def setUp(self):
        super(HeatTasksTests, self).setUp()
        self.heat_client = mock.MagicMock(name='heat_client')

    def _get_create_stack_flow(self, heat_client):
        flow = linear_flow.Flow('create stack flow')
        flow.add(heat_tasks.CreateStack(os_client=heat_client, requires=('stack_name', 'parameters', 'template', 'files'), provides='new_stack'))
        return flow

    def _get_update_stack_flow(self, heat_client):
        flow = linear_flow.Flow('update stack flow')
        flow.add(heat_tasks.UpdateStack(os_client=heat_client, requires=('stack_id', 'parameters', 'template', 'files')))
        return flow

    def _get_delete_stack_flow(self, heat_client):
        flow = linear_flow.Flow('delete stack flow')
        flow.add(heat_tasks.DeleteStack(os_client=heat_client, requires='stack_id'))
        return flow

    def test_create_stack(self):
        heat_client = mock.MagicMock(name='heat_client')
        stack_id = 'stack_id'
        stack_name = 'stack_name'
        stack = {'stack': {'id': stack_id}}
        heat_client.stacks.create.return_value = stack
        flow_store = {'stack_name': stack_name, 'parameters': 'parameters', 'template': 'template', 'files': 'files'}
        flow = self._get_create_stack_flow(heat_client)
        result = engines.run(flow, store=flow_store)
        heat_client.stacks.create.assert_called_once_with(**flow_store)
        self.assertEqual(stack_id, result['new_stack']['stack']['id'])

    def test_create_stack_with_error(self):
        heat_client = mock.MagicMock(name='heat_client')
        heat_client.stacks.create.side_effect = ValueError
        stack_name = 'stack_name'
        flow_store = {'stack_name': stack_name, 'parameters': 'parameters', 'template': 'template', 'files': 'files'}
        flow = self._get_create_stack_flow(heat_client)
        self.assertRaises(ValueError, engines.run, flow, store=flow_store)

    def test_update_stack(self):
        heat_client = mock.MagicMock(name='heat_client')
        stack_id = 'stack_id'
        flow_store = {'stack_id': stack_id, 'parameters': 'parameters', 'template': 'template', 'files': 'files'}
        flow = self._get_update_stack_flow(heat_client)
        expected_params = dict(flow_store)
        del expected_params['stack_id']
        engines.run(flow, store=flow_store)
        heat_client.stacks.update.assert_called_once_with(stack_id, **expected_params)

    def test_update_stack_with_error(self):
        heat_client = mock.MagicMock(name='heat_client')
        heat_client.stacks.update.side_effect = ValueError
        stack_id = 'stack_id'
        flow_store = {'stack_id': stack_id, 'parameters': 'parameters', 'template': 'template', 'files': 'files'}
        flow = self._get_update_stack_flow(heat_client)
        self.assertRaises(ValueError, engines.run, flow, store=flow_store)

    def test_delete_stack(self):
        heat_client = mock.MagicMock(name='heat_client')
        stack_id = 'stack_id'
        flow_store = {'stack_id': stack_id}
        flow = self._get_delete_stack_flow(heat_client)
        engines.run(flow, store=flow_store)
        heat_client.stacks.delete.assert_called_once_with(stack_id)

    def test_delete_stack_with_error(self):
        heat_client = mock.MagicMock(name='heat_client')
        heat_client.stacks.delete.side_effect = ValueError
        stack_id = 'stack_id'
        flow_store = {'stack_id': stack_id}
        flow = self._get_delete_stack_flow(heat_client)
        self.assertRaises(ValueError, engines.run, flow, store=flow_store)