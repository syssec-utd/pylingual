from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest

class SetStatusRequest(JDCloudRequest):
    """
    设置任务状态

    """

    def __init__(self, parameters, header=None, version='v1'):
        super(SetStatusRequest, self).__init__('/regions/{regionId}/task:setStatus', 'POST', header, version)
        self.parameters = parameters

class SetStatusParameters(object):

    def __init__(self, regionId, vo):
        """
        :param regionId: 地域ID
        :param vo: 设置任务状态
        """
        self.regionId = regionId
        self.vo = vo