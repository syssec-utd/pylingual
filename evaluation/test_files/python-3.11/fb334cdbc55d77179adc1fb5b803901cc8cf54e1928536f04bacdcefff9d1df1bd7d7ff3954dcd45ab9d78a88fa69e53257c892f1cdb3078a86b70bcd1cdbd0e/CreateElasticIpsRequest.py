from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest

class CreateElasticIpsRequest(JDCloudRequest):
    """
    创建一个或者多个弹性公网IP
    """

    def __init__(self, parameters, header=None, version='v1'):
        super(CreateElasticIpsRequest, self).__init__('/regions/{regionId}/elasticIps/', 'POST', header, version)
        self.parameters = parameters

class CreateElasticIpsParameters(object):

    def __init__(self, regionId, maxCount, elasticIpSpec):
        """
        :param regionId: Region ID
        :param maxCount: 购买弹性ip数量；取值范围：[1,100]
        :param elasticIpSpec: 弹性ip规格
        """
        self.regionId = regionId
        self.maxCount = maxCount
        self.elasticIpAddress = None
        self.elasticIpSpec = elasticIpSpec
        self.userTags = None
        self.ipType = None
        self.resourceGroupId = None
        self.dryRun = None

    def setElasticIpAddress(self, elasticIpAddress):
        """
        :param elasticIpAddress: (Optional) 指定弹性ip地址进行创建，当申请创建多个弹性ip时，必须为空
        """
        self.elasticIpAddress = elasticIpAddress

    def setUserTags(self, userTags):
        """
        :param userTags: (Optional) 用户标签
        """
        self.userTags = userTags

    def setIpType(self, ipType):
        """
        :param ipType: (Optional) 弹性ip类型，取值：standard(标准公网IP)，edge(边缘公网IP)，默认为standard
        """
        self.ipType = ipType

    def setResourceGroupId(self, resourceGroupId):
        """
        :param resourceGroupId: (Optional) 资源所属资源组ID
        """
        self.resourceGroupId = resourceGroupId

    def setDryRun(self, dryRun):
        """
        :param dryRun: (Optional) 预检标识，默认false，dryRun为true时只作检查，不做变更
        """
        self.dryRun = dryRun