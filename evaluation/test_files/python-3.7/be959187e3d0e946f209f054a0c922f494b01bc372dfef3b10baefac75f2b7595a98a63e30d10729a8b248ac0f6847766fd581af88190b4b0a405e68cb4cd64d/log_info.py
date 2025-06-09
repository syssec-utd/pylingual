import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class LogInfo:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'name': 'str', 'url': 'str', 'size': 'int', 'start_time': 'str', 'end_time': 'str'}
    attribute_map = {'name': 'name', 'url': 'url', 'size': 'size', 'start_time': 'start_time', 'end_time': 'end_time'}

    def __init__(self, name=None, url=None, size=None, start_time=None, end_time=None):
        """LogInfo

        The model defined in huaweicloud sdk

        :param name: 日志文件名，打包文件名格式：{Domain}_{logStartTimeStamp}.log.gz
        :type name: str
        :param url: 日志下载链接
        :type url: str
        :param size: 日志文件大小
        :type size: int
        :param start_time: 日志文件中日志开始时间，北京时间
        :type start_time: str
        :param end_time: 日志文件中日志结束时间，北京时间
        :type end_time: str
        """
        self._name = None
        self._url = None
        self._size = None
        self._start_time = None
        self._end_time = None
        self.discriminator = None
        self.name = name
        self.url = url
        self.size = size
        self.start_time = start_time
        self.end_time = end_time

    @property
    def name(self):
        """Gets the name of this LogInfo.

        日志文件名，打包文件名格式：{Domain}_{logStartTimeStamp}.log.gz

        :return: The name of this LogInfo.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LogInfo.

        日志文件名，打包文件名格式：{Domain}_{logStartTimeStamp}.log.gz

        :param name: The name of this LogInfo.
        :type name: str
        """
        self._name = name

    @property
    def url(self):
        """Gets the url of this LogInfo.

        日志下载链接

        :return: The url of this LogInfo.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this LogInfo.

        日志下载链接

        :param url: The url of this LogInfo.
        :type url: str
        """
        self._url = url

    @property
    def size(self):
        """Gets the size of this LogInfo.

        日志文件大小

        :return: The size of this LogInfo.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this LogInfo.

        日志文件大小

        :param size: The size of this LogInfo.
        :type size: int
        """
        self._size = size

    @property
    def start_time(self):
        """Gets the start_time of this LogInfo.

        日志文件中日志开始时间，北京时间

        :return: The start_time of this LogInfo.
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this LogInfo.

        日志文件中日志开始时间，北京时间

        :param start_time: The start_time of this LogInfo.
        :type start_time: str
        """
        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this LogInfo.

        日志文件中日志结束时间，北京时间

        :return: The end_time of this LogInfo.
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this LogInfo.

        日志文件中日志结束时间，北京时间

        :param end_time: The end_time of this LogInfo.
        :type end_time: str
        """
        self._end_time = end_time

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}
        for (attr, _) in six.iteritems(self.openapi_types):
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
        if not isinstance(other, LogInfo):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other