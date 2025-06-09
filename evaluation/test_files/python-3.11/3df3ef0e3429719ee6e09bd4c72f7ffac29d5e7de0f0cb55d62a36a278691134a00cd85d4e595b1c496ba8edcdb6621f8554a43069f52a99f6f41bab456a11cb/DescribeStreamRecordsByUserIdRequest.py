from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest

class DescribeStreamRecordsByUserIdRequest(JDCloudRequest):
    """
    查询指定用户在房间内的推流历史记录
允许通过条件过滤查询，支持的过滤字段如下：
           - kind[eq] 在线状态 1-音频流 2-视频流 100-数据流
           - startTime[eq] 用户推流开始时间-UTC时间  startTime,endTime同时指定时生效
           - endTime[eq]   用户推流结束时间-UTC时间  startTime,endTime同时指定时生效

    """

    def __init__(self, parameters, header=None, version='v1'):
        super(DescribeStreamRecordsByUserIdRequest, self).__init__('/describeStreamRecordsByUserId/{appId}', 'GET', header, version)
        self.parameters = parameters

class DescribeStreamRecordsByUserIdParameters(object):

    def __init__(self, appId, userRoomId, userId):
        """
        :param appId: 应用ID
        :param userRoomId: 业务接入方定义的且在JRTC系统内注册过的房间号
        :param userId: 业务接入方用户体系定义的且在JRTC系统内注册过的userId
        """
        self.appId = appId
        self.pageNumber = None
        self.pageSize = None
        self.userRoomId = userRoomId
        self.userId = userId
        self.filters = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码；默认值为 1
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小；默认值为 10；取值范围 [10, 100]
        """
        self.pageSize = pageSize

    def setFilters(self, filters):
        """
        :param filters: (Optional) 传参字段描述:
- kind[eq] 在线状态 1-音频流 2-视频流 100-数据流
- startTime[eq] 用户推流开始时间-UTC时间  startTime,endTime同时指定时生效
- endTime[eq]   用户推流结束时间-UTC时间  startTime,endTime同时指定时生效

        """
        self.filters = filters