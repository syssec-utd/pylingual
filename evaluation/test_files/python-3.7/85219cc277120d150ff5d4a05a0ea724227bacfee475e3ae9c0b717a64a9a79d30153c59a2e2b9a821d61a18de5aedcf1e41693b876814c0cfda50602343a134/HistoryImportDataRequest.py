from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest

class HistoryImportDataRequest(JDCloudRequest):
    """
    获取当前实例用户查询导入数据sql历史
    """

    def __init__(self, parameters, header=None, version='v1'):
        super(HistoryImportDataRequest, self).__init__('/regions/{regionId}/historyImportData', 'POST', header, version)
        self.parameters = parameters

class HistoryImportDataParameters(object):

    def __init__(self, regionId):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》](../Enum-Definitions/Regions-AZ.md)
        """
        self.regionId = regionId
        self.dataSourceId = None
        self.dbName = None
        self.pageNumber = None
        self.pageSize = None

    def setDataSourceId(self, dataSourceId):
        """
        :param dataSourceId: (Optional) 数据源id
        """
        self.dataSourceId = dataSourceId

    def setDbName(self, dbName):
        """
        :param dbName: (Optional) 数据库名称
        """
        self.dbName = dbName

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 显示数据的页码，取值范围：[1,∞)。pageNumber为Null时，返回所有数据页码；超过总页数时，无数据。
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 每页显示的数据条数，用于查询列表的接口。
        """
        self.pageSize = pageSize