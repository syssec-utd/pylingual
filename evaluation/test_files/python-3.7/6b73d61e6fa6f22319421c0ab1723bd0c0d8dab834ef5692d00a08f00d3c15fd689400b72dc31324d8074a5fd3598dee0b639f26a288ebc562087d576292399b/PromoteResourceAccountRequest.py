from aliyunsdkcore.request import RpcRequest
from aliyunsdkresourcemanager.endpoint import endpoint_data

class PromoteResourceAccountRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'ResourceManager', '2020-03-31', 'PromoteResourceAccount')
        self.set_protocol_type('https')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_AccountId(self):
        return self.get_query_params().get('AccountId')

    def set_AccountId(self, AccountId):
        self.add_query_param('AccountId', AccountId)

    def get_Email(self):
        return self.get_query_params().get('Email')

    def set_Email(self, Email):
        self.add_query_param('Email', Email)