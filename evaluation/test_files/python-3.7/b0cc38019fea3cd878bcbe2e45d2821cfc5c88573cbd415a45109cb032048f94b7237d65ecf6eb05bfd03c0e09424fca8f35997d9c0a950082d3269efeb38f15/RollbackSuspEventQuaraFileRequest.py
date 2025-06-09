from aliyunsdkcore.request import RpcRequest
from aliyunsdkecd.endpoint import endpoint_data

class RollbackSuspEventQuaraFileRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'ecd', '2020-09-30', 'RollbackSuspEventQuaraFile')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_QuaraFieldId(self):
        return self.get_query_params().get('QuaraFieldId')

    def set_QuaraFieldId(self, QuaraFieldId):
        self.add_query_param('QuaraFieldId', QuaraFieldId)

    def get_DesktopId(self):
        return self.get_query_params().get('DesktopId')

    def set_DesktopId(self, DesktopId):
        self.add_query_param('DesktopId', DesktopId)