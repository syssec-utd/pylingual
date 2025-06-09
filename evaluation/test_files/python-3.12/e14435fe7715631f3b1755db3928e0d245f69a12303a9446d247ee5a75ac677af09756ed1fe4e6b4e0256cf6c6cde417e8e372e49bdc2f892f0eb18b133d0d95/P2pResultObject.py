class P2pResultObject(object):

    def __init__(self, pageNumber=None, pageSize=None, totalCount=None, p2pConfigs=None):
        """
        :param pageNumber: (Optional) 当前页码
        :param pageSize: (Optional) 每页数量
        :param totalCount: (Optional) 查询总数
        :param p2pConfigs: (Optional) P2P配置集合
        """
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalCount = totalCount
        self.p2pConfigs = p2pConfigs