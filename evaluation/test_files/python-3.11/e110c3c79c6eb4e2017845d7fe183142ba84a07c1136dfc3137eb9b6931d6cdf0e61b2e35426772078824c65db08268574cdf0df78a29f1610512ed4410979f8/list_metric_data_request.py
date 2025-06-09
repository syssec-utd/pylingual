import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class ListMetricDataRequest:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'instance_id': 'str', 'dim': 'str', 'metric_name': 'str', '_from': 'str', 'to': 'str', 'period': 'int', 'filter': 'str'}
    attribute_map = {'instance_id': 'instance_id', 'dim': 'dim', 'metric_name': 'metric_name', '_from': 'from', 'to': 'to', 'period': 'period', 'filter': 'filter'}

    def __init__(self, instance_id=None, dim=None, metric_name=None, _from=None, to=None, period=None, filter=None):
        """ListMetricDataRequest

        The model defined in huaweicloud sdk

        :param instance_id: 实例ID
        :type instance_id: str
        :param dim: 指标维度 - inbound_eip：入口公网带宽，仅ELB类型实例支持 - outbound_eip：出口公网带宽
        :type dim: str
        :param metric_name: 指标名称 - upstream_bandwidth：出网带宽 - downstream_bandwidth：入网带宽 - upstream_bandwidth_usage：出网带宽使用率 - downstream_bandwidth_usage：入网带宽使用率 - up_stream：出网流量 - down_stream：入网流量
        :type metric_name: str
        :param _from: 查询数据起始时间，UNIX时间戳，单位毫秒。
        :type _from: str
        :param to: 查询数据截止时间UNIX时间戳，单位毫秒。from必须小于to。
        :type to: str
        :param period: 监控数据粒度。 - 1：实时数据 - 300：5分钟粒度 - 1200：20分钟粒度 - 3600：1小时粒度 - 14400：4小时粒度 - 86400：1天粒度
        :type period: int
        :param filter: 数据聚合方式。 - average：聚合周期内指标数据的平均值。 - max：聚合周期内指标数据的最大值。 - min：聚合周期内指标数据的最小值。 - sum：聚合周期内指标数据的求和值。 - variance：聚合周期内指标数据的方差。
        :type filter: str
        """
        self._instance_id = None
        self._dim = None
        self._metric_name = None
        self.__from = None
        self._to = None
        self._period = None
        self._filter = None
        self.discriminator = None
        self.instance_id = instance_id
        self.dim = dim
        self.metric_name = metric_name
        self._from = _from
        self.to = to
        self.period = period
        self.filter = filter

    @property
    def instance_id(self):
        """Gets the instance_id of this ListMetricDataRequest.

        实例ID

        :return: The instance_id of this ListMetricDataRequest.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ListMetricDataRequest.

        实例ID

        :param instance_id: The instance_id of this ListMetricDataRequest.
        :type instance_id: str
        """
        self._instance_id = instance_id

    @property
    def dim(self):
        """Gets the dim of this ListMetricDataRequest.

        指标维度 - inbound_eip：入口公网带宽，仅ELB类型实例支持 - outbound_eip：出口公网带宽

        :return: The dim of this ListMetricDataRequest.
        :rtype: str
        """
        return self._dim

    @dim.setter
    def dim(self, dim):
        """Sets the dim of this ListMetricDataRequest.

        指标维度 - inbound_eip：入口公网带宽，仅ELB类型实例支持 - outbound_eip：出口公网带宽

        :param dim: The dim of this ListMetricDataRequest.
        :type dim: str
        """
        self._dim = dim

    @property
    def metric_name(self):
        """Gets the metric_name of this ListMetricDataRequest.

        指标名称 - upstream_bandwidth：出网带宽 - downstream_bandwidth：入网带宽 - upstream_bandwidth_usage：出网带宽使用率 - downstream_bandwidth_usage：入网带宽使用率 - up_stream：出网流量 - down_stream：入网流量

        :return: The metric_name of this ListMetricDataRequest.
        :rtype: str
        """
        return self._metric_name

    @metric_name.setter
    def metric_name(self, metric_name):
        """Sets the metric_name of this ListMetricDataRequest.

        指标名称 - upstream_bandwidth：出网带宽 - downstream_bandwidth：入网带宽 - upstream_bandwidth_usage：出网带宽使用率 - downstream_bandwidth_usage：入网带宽使用率 - up_stream：出网流量 - down_stream：入网流量

        :param metric_name: The metric_name of this ListMetricDataRequest.
        :type metric_name: str
        """
        self._metric_name = metric_name

    @property
    def _from(self):
        """Gets the _from of this ListMetricDataRequest.

        查询数据起始时间，UNIX时间戳，单位毫秒。

        :return: The _from of this ListMetricDataRequest.
        :rtype: str
        """
        return self.__from

    @_from.setter
    def _from(self, _from):
        """Sets the _from of this ListMetricDataRequest.

        查询数据起始时间，UNIX时间戳，单位毫秒。

        :param _from: The _from of this ListMetricDataRequest.
        :type _from: str
        """
        self.__from = _from

    @property
    def to(self):
        """Gets the to of this ListMetricDataRequest.

        查询数据截止时间UNIX时间戳，单位毫秒。from必须小于to。

        :return: The to of this ListMetricDataRequest.
        :rtype: str
        """
        return self._to

    @to.setter
    def to(self, to):
        """Sets the to of this ListMetricDataRequest.

        查询数据截止时间UNIX时间戳，单位毫秒。from必须小于to。

        :param to: The to of this ListMetricDataRequest.
        :type to: str
        """
        self._to = to

    @property
    def period(self):
        """Gets the period of this ListMetricDataRequest.

        监控数据粒度。 - 1：实时数据 - 300：5分钟粒度 - 1200：20分钟粒度 - 3600：1小时粒度 - 14400：4小时粒度 - 86400：1天粒度

        :return: The period of this ListMetricDataRequest.
        :rtype: int
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this ListMetricDataRequest.

        监控数据粒度。 - 1：实时数据 - 300：5分钟粒度 - 1200：20分钟粒度 - 3600：1小时粒度 - 14400：4小时粒度 - 86400：1天粒度

        :param period: The period of this ListMetricDataRequest.
        :type period: int
        """
        self._period = period

    @property
    def filter(self):
        """Gets the filter of this ListMetricDataRequest.

        数据聚合方式。 - average：聚合周期内指标数据的平均值。 - max：聚合周期内指标数据的最大值。 - min：聚合周期内指标数据的最小值。 - sum：聚合周期内指标数据的求和值。 - variance：聚合周期内指标数据的方差。

        :return: The filter of this ListMetricDataRequest.
        :rtype: str
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """Sets the filter of this ListMetricDataRequest.

        数据聚合方式。 - average：聚合周期内指标数据的平均值。 - max：聚合周期内指标数据的最大值。 - min：聚合周期内指标数据的最小值。 - sum：聚合周期内指标数据的求和值。 - variance：聚合周期内指标数据的方差。

        :param filter: The filter of this ListMetricDataRequest.
        :type filter: str
        """
        self._filter = filter

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}
        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, 'to_dict') else x, value))
            elif hasattr(value, 'to_dict'):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(lambda item: (item[0], item[1].to_dict()) if hasattr(item[1], 'to_dict') else item, value.items()))
            elif attr in self.sensitive_list:
                result[attr] = '****'
            else:
                result[attr] = value
        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding('utf-8')
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ListMetricDataRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other