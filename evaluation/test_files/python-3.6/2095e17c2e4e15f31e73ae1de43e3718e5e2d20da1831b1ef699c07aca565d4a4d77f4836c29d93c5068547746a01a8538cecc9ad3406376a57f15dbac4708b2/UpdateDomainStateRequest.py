from aliyunsdkcore.request import RpcRequest
from aliyunsdkga.endpoint import endpoint_data

class UpdateDomainStateRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'Ga', '2019-11-20', 'UpdateDomainState', 'gaplus')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_Domain(self):
        return self.get_query_params().get('Domain')

    def set_Domain(self, Domain):
        self.add_query_param('Domain', Domain)