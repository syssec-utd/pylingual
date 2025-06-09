from servicecatalog_puppet.workflow import tasks_unit_tests_helper

class SimulatePolicyForAccountAndRegionTaskTest(tasks_unit_tests_helper.PuppetTaskUnitTest):
    account_id = 'account_id'
    region = 'region'
    puppet_account_id = 'puppet_account_id'
    simulate_policy_name = 'simulate_policy_name'
    manifest_file_path = 'manifest_file_path'

    def setUp(self) -> None:
        from servicecatalog_puppet.workflow.simulate_policies import simulate_policy_for_account_and_region_task
        self.module = simulate_policy_for_account_and_region_task
        self.sut = self.module.SimulatePolicyForAccountAndRegionTask(manifest_file_path=self.manifest_file_path, simulate_policy_name=self.simulate_policy_name, puppet_account_id=self.puppet_account_id, account_id=self.account_id, region=self.region)
        self.wire_up_mocks()

    def test_params_for_results_display(self):
        expected_result = {'puppet_account_id': self.puppet_account_id, 'simulate_policy_name': self.simulate_policy_name, 'region': self.region, 'account_id': self.account_id, 'cache_invalidator': self.cache_invalidator}
        actual_result = self.sut.params_for_results_display()
        self.assertEqual(expected_result, actual_result)