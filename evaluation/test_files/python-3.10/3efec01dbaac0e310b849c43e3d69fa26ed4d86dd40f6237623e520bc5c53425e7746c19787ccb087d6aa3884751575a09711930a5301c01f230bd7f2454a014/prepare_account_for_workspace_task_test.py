from unittest import skip
from servicecatalog_puppet.workflow import tasks_unit_tests_helper

class PrepareAccountForWorkspaceTaskTest(tasks_unit_tests_helper.PuppetTaskUnitTest):
    account_id = 'account_id'

    def setUp(self) -> None:
        from servicecatalog_puppet.workflow.workspaces import prepare_account_for_workspace_task
        self.module = prepare_account_for_workspace_task
        self.sut = self.module.PrepareAccountForWorkspaceTask(**self.get_common_args(), account_id=self.account_id)
        self.wire_up_mocks()

    def test_params_for_results_display(self):
        expected_result = {'account_id': self.account_id}
        actual_result = self.sut.params_for_results_display()
        self.assertEqual(expected_result, actual_result)

    @skip
    def test_run(self):
        actual_result = self.sut.run()
        raise NotImplementedError()