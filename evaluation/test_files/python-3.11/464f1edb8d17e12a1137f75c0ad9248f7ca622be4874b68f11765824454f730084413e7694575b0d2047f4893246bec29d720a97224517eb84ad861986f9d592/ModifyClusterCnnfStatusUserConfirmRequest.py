from aliyunsdkcore.request import RpcRequest
from aliyunsdksas.endpoint import endpoint_data

class ModifyClusterCnnfStatusUserConfirmRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'Sas', '2018-12-03', 'ModifyClusterCnnfStatusUserConfirm')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_ClusterIdss(self):
        return self.get_query_params().get('ClusterIds')

    def set_ClusterIdss(self, ClusterIds):
        for depth1 in range(len(ClusterIds)):
            self.add_query_param('ClusterIds.' + str(depth1 + 1), ClusterIds[depth1])

    def get_UserConfirm(self):
        return self.get_query_params().get('UserConfirm')

    def set_UserConfirm(self, UserConfirm):
        self.add_query_param('UserConfirm', UserConfirm)