from aliyunsdkcore.request import RoaRequest
from aliyunsdkeas.endpoint import endpoint_data

class DescribeServiceAutoScalerRequest(RoaRequest):

    def __init__(self):
        RoaRequest.__init__(self, 'eas', '2021-07-01', 'DescribeServiceAutoScaler', 'eas')
        self.set_uri_pattern('/api/v2/services/[ClusterId]/[ServiceName]/autoscaler')
        self.set_method('GET')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_ServiceName(self):
        return self.get_path_params().get('ServiceName')

    def set_ServiceName(self, ServiceName):
        self.add_path_param('ServiceName', ServiceName)

    def get_ClusterId(self):
        return self.get_path_params().get('ClusterId')

    def set_ClusterId(self, ClusterId):
        self.add_path_param('ClusterId', ClusterId)