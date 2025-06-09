from aliyunsdkcore.request import RpcRequest
from aliyunsdkmse.endpoint import endpoint_data

class ListListenersByIpRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'mse', '2019-05-31', 'ListListenersByIp', 'mse')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_Ip(self):
        return self.get_query_params().get('Ip')

    def set_Ip(self, Ip):
        self.add_query_param('Ip', Ip)

    def get_InstanceId(self):
        return self.get_query_params().get('InstanceId')

    def set_InstanceId(self, InstanceId):
        self.add_query_param('InstanceId', InstanceId)

    def get_NamespaceId(self):
        return self.get_query_params().get('NamespaceId')

    def set_NamespaceId(self, NamespaceId):
        self.add_query_param('NamespaceId', NamespaceId)

    def get_RequestPars(self):
        return self.get_query_params().get('RequestPars')

    def set_RequestPars(self, RequestPars):
        self.add_query_param('RequestPars', RequestPars)

    def get_AcceptLanguage(self):
        return self.get_query_params().get('AcceptLanguage')

    def set_AcceptLanguage(self, AcceptLanguage):
        self.add_query_param('AcceptLanguage', AcceptLanguage)