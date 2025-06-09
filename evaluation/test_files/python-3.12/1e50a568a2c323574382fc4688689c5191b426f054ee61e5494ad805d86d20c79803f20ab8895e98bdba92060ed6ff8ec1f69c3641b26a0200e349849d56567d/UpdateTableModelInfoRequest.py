from aliyunsdkcore.request import RpcRequest
from aliyunsdkdataworks_public.endpoint import endpoint_data

class UpdateTableModelInfoRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'dataworks-public', '2020-05-18', 'UpdateTableModelInfo')
        self.set_method('POST')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_LevelType(self):
        return self.get_query_params().get('LevelType')

    def set_LevelType(self, LevelType):
        self.add_query_param('LevelType', LevelType)

    def get_SecondLevelThemeId(self):
        return self.get_query_params().get('SecondLevelThemeId')

    def set_SecondLevelThemeId(self, SecondLevelThemeId):
        self.add_query_param('SecondLevelThemeId', SecondLevelThemeId)

    def get_TableGuid(self):
        return self.get_query_params().get('TableGuid')

    def set_TableGuid(self, TableGuid):
        self.add_query_param('TableGuid', TableGuid)

    def get_LevelId(self):
        return self.get_query_params().get('LevelId')

    def set_LevelId(self, LevelId):
        self.add_query_param('LevelId', LevelId)

    def get_FirstLevelThemeId(self):
        return self.get_query_params().get('FirstLevelThemeId')

    def set_FirstLevelThemeId(self, FirstLevelThemeId):
        self.add_query_param('FirstLevelThemeId', FirstLevelThemeId)