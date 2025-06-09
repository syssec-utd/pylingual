from aliyunsdkcore.request import RpcRequest

class ApproveOtaTaskRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'appstream-center', '2021-09-01', 'ApproveOtaTask')
        self.set_method('POST')

    def get_BizRegionId(self):
        return self.get_body_params().get('BizRegionId')

    def set_BizRegionId(self, BizRegionId):
        self.add_body_params('BizRegionId', BizRegionId)

    def get_OtaType(self):
        return self.get_body_params().get('OtaType')

    def set_OtaType(self, OtaType):
        self.add_body_params('OtaType', OtaType)

    def get_StartTime(self):
        return self.get_body_params().get('StartTime')

    def set_StartTime(self, StartTime):
        self.add_body_params('StartTime', StartTime)

    def get_AppInstanceGroupId(self):
        return self.get_body_params().get('AppInstanceGroupId')

    def set_AppInstanceGroupId(self, AppInstanceGroupId):
        self.add_body_params('AppInstanceGroupId', AppInstanceGroupId)

    def get_TaskId(self):
        return self.get_body_params().get('TaskId')

    def set_TaskId(self, TaskId):
        self.add_body_params('TaskId', TaskId)