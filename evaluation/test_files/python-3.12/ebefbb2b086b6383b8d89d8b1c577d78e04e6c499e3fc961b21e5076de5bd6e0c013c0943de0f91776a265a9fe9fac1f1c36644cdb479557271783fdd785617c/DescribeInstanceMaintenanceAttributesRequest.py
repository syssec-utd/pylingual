from aliyunsdkcore.request import RpcRequest
from aliyunsdkecs.endpoint import endpoint_data

class DescribeInstanceMaintenanceAttributesRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'Ecs', '2014-05-26', 'DescribeInstanceMaintenanceAttributes', 'ecs')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_ResourceOwnerId(self):
        return self.get_query_params().get('ResourceOwnerId')

    def set_ResourceOwnerId(self, ResourceOwnerId):
        self.add_query_param('ResourceOwnerId', ResourceOwnerId)

    def get_PageNumber(self):
        return self.get_query_params().get('PageNumber')

    def set_PageNumber(self, PageNumber):
        self.add_query_param('PageNumber', PageNumber)

    def get_PageSize(self):
        return self.get_query_params().get('PageSize')

    def set_PageSize(self, PageSize):
        self.add_query_param('PageSize', PageSize)

    def get_ResourceOwnerAccount(self):
        return self.get_query_params().get('ResourceOwnerAccount')

    def set_ResourceOwnerAccount(self, ResourceOwnerAccount):
        self.add_query_param('ResourceOwnerAccount', ResourceOwnerAccount)

    def get_OwnerAccount(self):
        return self.get_query_params().get('OwnerAccount')

    def set_OwnerAccount(self, OwnerAccount):
        self.add_query_param('OwnerAccount', OwnerAccount)

    def get_OwnerId(self):
        return self.get_query_params().get('OwnerId')

    def set_OwnerId(self, OwnerId):
        self.add_query_param('OwnerId', OwnerId)

    def get_InstanceIds(self):
        return self.get_query_params().get('InstanceId')

    def set_InstanceIds(self, InstanceId):
        for depth1 in range(len(InstanceId)):
            self.add_query_param('InstanceId.' + str(depth1 + 1), InstanceId[depth1])