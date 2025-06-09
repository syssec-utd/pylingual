class SnapshotTemplatePageInfo(object):

    def __init__(self, pageNumber=None, pageSize=None, totalElements=None, totalPages=None, content=None):
        """
        :param pageNumber: (Optional) 当前页码
        :param pageSize: (Optional) 每页数量
        :param totalElements: (Optional) 查询总数
        :param totalPages: (Optional) 总页数
        :param content: (Optional) 分页内容
        """
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalElements = totalElements
        self.totalPages = totalPages
        self.content = content