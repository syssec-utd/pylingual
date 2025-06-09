from aliyunsdkcore.request import RpcRequest
from aliyunsdkdcdn.endpoint import endpoint_data

class DescribeDcdnDomainRegionDataRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'dcdn', '2018-01-15', 'DescribeDcdnDomainRegionData')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_StartTime(self):
        return self.get_query_params().get('StartTime')

    def set_StartTime(self, StartTime):
        self.add_query_param('StartTime', StartTime)

    def get_DomainName(self):
        return self.get_query_params().get('DomainName')

    def set_DomainName(self, DomainName):
        self.add_query_param('DomainName', DomainName)

    def get_EndTime(self):
        return self.get_query_params().get('EndTime')

    def set_EndTime(self, EndTime):
        self.add_query_param('EndTime', EndTime)

    def get_OwnerId(self):
        return self.get_query_params().get('OwnerId')

    def set_OwnerId(self, OwnerId):
        self.add_query_param('OwnerId', OwnerId)