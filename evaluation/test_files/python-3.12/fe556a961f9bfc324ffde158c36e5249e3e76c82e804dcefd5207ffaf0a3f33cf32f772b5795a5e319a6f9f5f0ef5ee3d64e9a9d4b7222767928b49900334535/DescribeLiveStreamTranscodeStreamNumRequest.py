from aliyunsdkcore.request import RpcRequest
from aliyunsdklive.endpoint import endpoint_data

class DescribeLiveStreamTranscodeStreamNumRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'live', '2016-11-01', 'DescribeLiveStreamTranscodeStreamNum', 'live')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_DomainName(self):
        return self.get_query_params().get('DomainName')

    def set_DomainName(self, DomainName):
        self.add_query_param('DomainName', DomainName)

    def get_OwnerId(self):
        return self.get_query_params().get('OwnerId')

    def set_OwnerId(self, OwnerId):
        self.add_query_param('OwnerId', OwnerId)