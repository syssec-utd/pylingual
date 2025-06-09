from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest

class ModifyWhiteListRuleOfForwardRuleRequest(JDCloudRequest):
    """
    修改转发规则的白名单规则
    """

    def __init__(self, parameters, header=None, version='v1'):
        super(ModifyWhiteListRuleOfForwardRuleRequest, self).__init__('/regions/{regionId}/instances/{instanceId}/forwardRules/{forwardRuleId}/forwardWhiteListRule', 'PATCH', header, version)
        self.parameters = parameters

class ModifyWhiteListRuleOfForwardRuleParameters(object):

    def __init__(self, regionId, instanceId, forwardRuleId, modifySpec):
        """
        :param regionId: 区域 ID, 高防不区分区域, 传 cn-north-1 即可
        :param instanceId: 高防实例 Id
        :param forwardRuleId: 转发规则 Id
        :param modifySpec: 修改转发规则的黑名单规则请求参数
        """
        self.regionId = regionId
        self.instanceId = instanceId
        self.forwardRuleId = forwardRuleId
        self.modifySpec = modifySpec