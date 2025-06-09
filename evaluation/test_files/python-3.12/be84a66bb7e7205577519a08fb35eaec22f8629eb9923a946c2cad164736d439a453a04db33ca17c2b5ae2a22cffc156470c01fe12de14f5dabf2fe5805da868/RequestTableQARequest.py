from aliyunsdkcore.request import RpcRequest
from aliyunsdkalinlp.endpoint import endpoint_data

class RequestTableQARequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'alinlp', '2020-06-29', 'RequestTableQA', 'alinlp')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_Params(self):
        return self.get_body_params().get('Params')

    def set_Params(self, Params):
        self.add_body_params('Params', Params)

    def get_ServiceCode(self):
        return self.get_body_params().get('ServiceCode')

    def set_ServiceCode(self, ServiceCode):
        self.add_body_params('ServiceCode', ServiceCode)