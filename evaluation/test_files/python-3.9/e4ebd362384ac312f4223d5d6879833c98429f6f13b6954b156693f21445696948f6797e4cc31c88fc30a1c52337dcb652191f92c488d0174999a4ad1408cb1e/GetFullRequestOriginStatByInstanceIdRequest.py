from aliyunsdkcore.request import RpcRequest
from aliyunsdkdas.endpoint import endpoint_data

class GetFullRequestOriginStatByInstanceIdRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'DAS', '2020-01-16', 'GetFullRequestOriginStatByInstanceId')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_UserId(self):
        return self.get_query_params().get('UserId')

    def set_UserId(self, UserId):
        self.add_query_param('UserId', UserId)

    def get_InstanceId(self):
        return self.get_query_params().get('InstanceId')

    def set_InstanceId(self, InstanceId):
        self.add_query_param('InstanceId', InstanceId)

    def get_NodeId(self):
        return self.get_query_params().get('NodeId')

    def set_NodeId(self, NodeId):
        self.add_query_param('NodeId', NodeId)

    def get_Start(self):
        return self.get_query_params().get('Start')

    def set_Start(self, Start):
        self.add_query_param('Start', Start)

    def get_End(self):
        return self.get_query_params().get('End')

    def set_End(self, End):
        self.add_query_param('End', End)

    def get_OrderBy(self):
        return self.get_query_params().get('OrderBy')

    def set_OrderBy(self, OrderBy):
        self.add_query_param('OrderBy', OrderBy)

    def get_Asc(self):
        return self.get_query_params().get('Asc')

    def set_Asc(self, Asc):
        self.add_query_param('Asc', Asc)

    def get_PageNo(self):
        return self.get_query_params().get('PageNo')

    def set_PageNo(self, PageNo):
        self.add_query_param('PageNo', PageNo)

    def get_PageSize(self):
        return self.get_query_params().get('PageSize')

    def set_PageSize(self, PageSize):
        self.add_query_param('PageSize', PageSize)

    def get_SqlType(self):
        return self.get_query_params().get('SqlType')

    def set_SqlType(self, SqlType):
        self.add_query_param('SqlType', SqlType)

    def get_Role(self):
        return self.get_query_params().get('Role')

    def set_Role(self, Role):
        self.add_query_param('Role', Role)