from aliyunsdkcore.request import RpcRequest
from aliyunsdkecs.endpoint import endpoint_data

class ModifyDiskChargeTypeRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'Ecs', '2014-05-26', 'ModifyDiskChargeType', 'ecs')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_ResourceOwnerId(self):
        return self.get_query_params().get('ResourceOwnerId')

    def set_ResourceOwnerId(self, ResourceOwnerId):
        self.add_query_param('ResourceOwnerId', ResourceOwnerId)

    def get_ClientToken(self):
        return self.get_query_params().get('ClientToken')

    def set_ClientToken(self, ClientToken):
        self.add_query_param('ClientToken', ClientToken)

    def get_DiskChargeType(self):
        return self.get_query_params().get('DiskChargeType')

    def set_DiskChargeType(self, DiskChargeType):
        self.add_query_param('DiskChargeType', DiskChargeType)

    def get_DiskIds(self):
        return self.get_query_params().get('DiskIds')

    def set_DiskIds(self, DiskIds):
        self.add_query_param('DiskIds', DiskIds)

    def get_AutoPay(self):
        return self.get_query_params().get('AutoPay')

    def set_AutoPay(self, AutoPay):
        self.add_query_param('AutoPay', AutoPay)

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

    def get_InstanceId(self):
        return self.get_query_params().get('InstanceId')

    def set_InstanceId(self, InstanceId):
        self.add_query_param('InstanceId', InstanceId)