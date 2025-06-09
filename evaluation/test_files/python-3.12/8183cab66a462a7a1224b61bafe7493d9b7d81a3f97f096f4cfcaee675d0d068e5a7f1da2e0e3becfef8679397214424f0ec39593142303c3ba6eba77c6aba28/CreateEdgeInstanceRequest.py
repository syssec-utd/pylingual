from aliyunsdkcore.request import RpcRequest
from aliyunsdkiot.endpoint import endpoint_data

class CreateEdgeInstanceRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'Iot', '2018-01-20', 'CreateEdgeInstance')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_Spec(self):
        return self.get_query_params().get('Spec')

    def set_Spec(self, Spec):
        self.add_query_param('Spec', Spec)

    def get_IotInstanceId(self):
        return self.get_query_params().get('IotInstanceId')

    def set_IotInstanceId(self, IotInstanceId):
        self.add_query_param('IotInstanceId', IotInstanceId)

    def get_Tags(self):
        return self.get_query_params().get('Tags')

    def set_Tags(self, Tags):
        self.add_query_param('Tags', Tags)

    def get_Name(self):
        return self.get_query_params().get('Name')

    def set_Name(self, Name):
        self.add_query_param('Name', Name)