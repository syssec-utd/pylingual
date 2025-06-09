from aliyunsdkcore.request import RoaRequest
from aliyunsdksae.endpoint import endpoint_data

class ListPublishedServicesRequest(RoaRequest):

    def __init__(self):
        RoaRequest.__init__(self, 'sae', '2019-05-06', 'ListPublishedServices', 'serverless')
        self.set_uri_pattern('/pop/v1/sam/service/listPublishedServices')
        self.set_method('GET')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_AppId(self):
        return self.get_query_params().get('AppId')

    def set_AppId(self, AppId):
        self.add_query_param('AppId', AppId)