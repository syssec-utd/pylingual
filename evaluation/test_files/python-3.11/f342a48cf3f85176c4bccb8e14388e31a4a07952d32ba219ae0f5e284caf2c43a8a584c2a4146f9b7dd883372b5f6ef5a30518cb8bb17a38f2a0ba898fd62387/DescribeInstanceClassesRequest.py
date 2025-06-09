from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest

class DescribeInstanceClassesRequest(JDCloudRequest):
    """
    规格获取接口
    """

    def __init__(self, parameters, header=None, version='v1'):
        super(DescribeInstanceClassesRequest, self).__init__('/regions/{regionId}/instances:describeInstanceClasses', 'GET', header, version)
        self.parameters = parameters

class DescribeInstanceClassesParameters(object):

    def __init__(self, regionId, storageType):
        """
        :param regionId: 地域代码
        :param storageType: 存储类型,目前只支持本地SSD;
        """
        self.regionId = regionId
        self.storageType = storageType