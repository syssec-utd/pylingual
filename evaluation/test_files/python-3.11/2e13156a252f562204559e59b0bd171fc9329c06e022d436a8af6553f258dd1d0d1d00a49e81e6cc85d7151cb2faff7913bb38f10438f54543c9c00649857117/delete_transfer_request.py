import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class DeleteTransferRequest:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'log_transfer_id': 'str'}
    attribute_map = {'log_transfer_id': 'log_transfer_id'}

    def __init__(self, log_transfer_id=None):
        """DeleteTransferRequest

        The model defined in huaweicloud sdk

        :param log_transfer_id: 日志转储ID。获取ID有3种方式： 1. 调用查询日志转储接口，返回值有日志转储ID  2. 调用新增日志转储接口，返回值有日志转储ID 3. 调用删除日志转储接口，返回值有日志转储ID
        :type log_transfer_id: str
        """
        self._log_transfer_id = None
        self.discriminator = None
        self.log_transfer_id = log_transfer_id

    @property
    def log_transfer_id(self):
        """Gets the log_transfer_id of this DeleteTransferRequest.

        日志转储ID。获取ID有3种方式： 1. 调用查询日志转储接口，返回值有日志转储ID  2. 调用新增日志转储接口，返回值有日志转储ID 3. 调用删除日志转储接口，返回值有日志转储ID

        :return: The log_transfer_id of this DeleteTransferRequest.
        :rtype: str
        """
        return self._log_transfer_id

    @log_transfer_id.setter
    def log_transfer_id(self, log_transfer_id):
        """Sets the log_transfer_id of this DeleteTransferRequest.

        日志转储ID。获取ID有3种方式： 1. 调用查询日志转储接口，返回值有日志转储ID  2. 调用新增日志转储接口，返回值有日志转储ID 3. 调用删除日志转储接口，返回值有日志转储ID

        :param log_transfer_id: The log_transfer_id of this DeleteTransferRequest.
        :type log_transfer_id: str
        """
        self._log_transfer_id = log_transfer_id

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
        if not isinstance(other, DeleteTransferRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other