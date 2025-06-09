from aliyunsdkcore.request import RpcRequest
from aliyunsdkdcdn.endpoint import endpoint_data

class DescribeDcdnUserCertificateExpireCountRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'dcdn', '2018-01-15', 'DescribeDcdnUserCertificateExpireCount')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_OwnerId(self):
        return self.get_query_params().get('OwnerId')

    def set_OwnerId(self, OwnerId):
        self.add_query_param('OwnerId', OwnerId)