import unittest
import pytest
import azure.mgmt.network
from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy
AZURE_LOCATION = 'eastus'

@pytest.mark.live_test_only
class TestMgmtNetwork(AzureMgmtRecordedTestCase):

    def setup_method(self, method):
        self.mgmt_client = self.create_mgmt_client(azure.mgmt.network.NetworkManagementClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_network(self, resource_group):
        LOCATION_NAME = AZURE_LOCATION
        result = self.mgmt_client.available_service_aliases.list_by_resource_group(resource_group.name, LOCATION_NAME)
        result = self.mgmt_client.available_resource_group_delegations.list(resource_group.name, LOCATION_NAME)
        result = self.mgmt_client.available_service_aliases.list(LOCATION_NAME)
        result = self.mgmt_client.available_delegations.list(LOCATION_NAME)
if __name__ == '__main__':
    unittest.main()