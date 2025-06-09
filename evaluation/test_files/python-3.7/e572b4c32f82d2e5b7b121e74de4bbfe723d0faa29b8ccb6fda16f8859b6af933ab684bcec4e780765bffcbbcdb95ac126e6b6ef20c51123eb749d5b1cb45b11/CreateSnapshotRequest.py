from aliyunsdkcore.request import RpcRequest
from aliyunsdkecd.endpoint import endpoint_data

class CreateSnapshotRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'ecd', '2020-09-30', 'CreateSnapshot')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_Description(self):
        return self.get_query_params().get('Description')

    def set_Description(self, Description):
        self.add_query_param('Description', Description)

    def get_SourceDiskType(self):
        return self.get_query_params().get('SourceDiskType')

    def set_SourceDiskType(self, SourceDiskType):
        self.add_query_param('SourceDiskType', SourceDiskType)

    def get_SnapshotName(self):
        return self.get_query_params().get('SnapshotName')

    def set_SnapshotName(self, SnapshotName):
        self.add_query_param('SnapshotName', SnapshotName)

    def get_DesktopId(self):
        return self.get_query_params().get('DesktopId')

    def set_DesktopId(self, DesktopId):
        self.add_query_param('DesktopId', DesktopId)