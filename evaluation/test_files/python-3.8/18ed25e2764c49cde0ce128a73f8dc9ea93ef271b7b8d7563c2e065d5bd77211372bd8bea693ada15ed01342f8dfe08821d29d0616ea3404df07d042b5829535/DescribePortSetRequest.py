from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest

class DescribePortSetRequest(JDCloudRequest):
    """
    查询实例的端口库
    """

    def __init__(self, parameters, header=None, version='v1'):
        super(DescribePortSetRequest, self).__init__('/regions/{regionId}/instances/{instanceId}/portSets/{portSetId}', 'GET', header, version)
        self.parameters = parameters

class DescribePortSetParameters(object):

    def __init__(self, regionId, instanceId, portSetId):
        """
        :param regionId: 地域 Id, DDoS 防护包目前支持华北-北京, 华东-宿迁, 华东-上海
        :param instanceId: 防护包实例 Id
        :param portSetId: 端口库 Id
        """
        self.regionId = regionId
        self.instanceId = instanceId
        self.portSetId = portSetId