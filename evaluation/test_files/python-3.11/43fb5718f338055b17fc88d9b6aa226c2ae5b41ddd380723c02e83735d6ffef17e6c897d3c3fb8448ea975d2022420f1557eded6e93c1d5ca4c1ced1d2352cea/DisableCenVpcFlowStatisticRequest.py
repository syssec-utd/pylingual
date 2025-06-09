from aliyunsdkcore.request import RpcRequest
from aliyunsdkcbn.endpoint import endpoint_data

class DisableCenVpcFlowStatisticRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'Cbn', '2017-09-12', 'DisableCenVpcFlowStatistic')
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

    def get_CenId(self):
        return self.get_query_params().get('CenId')

    def set_CenId(self, CenId):
        self.add_query_param('CenId', CenId)

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