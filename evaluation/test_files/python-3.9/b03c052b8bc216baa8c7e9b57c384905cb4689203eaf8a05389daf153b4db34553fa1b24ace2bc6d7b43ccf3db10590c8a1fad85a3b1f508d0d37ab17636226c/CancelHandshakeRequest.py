from aliyunsdkcore.request import RpcRequest
from aliyunsdkresourcemanager.endpoint import endpoint_data

class CancelHandshakeRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'ResourceManager', '2020-03-31', 'CancelHandshake')
        self.set_protocol_type('https')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_HandshakeId(self):
        return self.get_query_params().get('HandshakeId')

    def set_HandshakeId(self, HandshakeId):
        self.add_query_param('HandshakeId', HandshakeId)