from aliyunsdkcore.request import RpcRequest
from aliyunsdkvpc.endpoint import endpoint_data

class CancelCommonBandwidthPackageIpBandwidthRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'Vpc', '2016-04-28', 'CancelCommonBandwidthPackageIpBandwidth', 'vpc')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_ResourceOwnerId(self):
        return self.get_query_params().get('ResourceOwnerId')

    def set_ResourceOwnerId(self, ResourceOwnerId):
        self.add_query_param('ResourceOwnerId', ResourceOwnerId)

    def get_BandwidthPackageId(self):
        return self.get_query_params().get('BandwidthPackageId')

    def set_BandwidthPackageId(self, BandwidthPackageId):
        self.add_query_param('BandwidthPackageId', BandwidthPackageId)

    def get_ResourceOwnerAccount(self):
        return self.get_query_params().get('ResourceOwnerAccount')

    def set_ResourceOwnerAccount(self, ResourceOwnerAccount):
        self.add_query_param('ResourceOwnerAccount', ResourceOwnerAccount)

    def get_OwnerAccount(self):
        return self.get_query_params().get('OwnerAccount')

    def set_OwnerAccount(self, OwnerAccount):
        self.add_query_param('OwnerAccount', OwnerAccount)

    def get_EipId(self):
        return self.get_query_params().get('EipId')

    def set_EipId(self, EipId):
        self.add_query_param('EipId', EipId)

    def get_OwnerId(self):
        return self.get_query_params().get('OwnerId')

    def set_OwnerId(self, OwnerId):
        self.add_query_param('OwnerId', OwnerId)