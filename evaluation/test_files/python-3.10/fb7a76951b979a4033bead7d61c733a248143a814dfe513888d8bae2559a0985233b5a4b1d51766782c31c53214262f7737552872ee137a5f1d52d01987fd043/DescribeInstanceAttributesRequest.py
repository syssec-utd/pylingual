from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest

class DescribeInstanceAttributesRequest(JDCloudRequest):
    """
    查询RDS实例（MySQL、SQL Server等）的详细信息以及MySQL/PostgreSQL只读实例详细信息
    """

    def __init__(self, parameters, header=None, version='v1'):
        super(DescribeInstanceAttributesRequest, self).__init__('/regions/{regionId}/instances/{instanceId}', 'GET', header, version)
        self.parameters = parameters

class DescribeInstanceAttributesParameters(object):

    def __init__(self, regionId, instanceId):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》](../Enum-Definitions/Regions-AZ.md)
        :param instanceId: RDS 实例ID，唯一标识一个RDS实例
        """
        self.regionId = regionId
        self.instanceId = instanceId