import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class UpdateInstanceConfigurationRequestBody:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'values': 'dict(str, str)'}
    attribute_map = {'values': 'values'}

    def __init__(self, values=None):
        """UpdateInstanceConfigurationRequestBody

        The model defined in huaweicloud sdk

        :param values: 参数值对象，用户基于默认参数模板自定义的参数值。为空时不修改参数值。  - key：参数名称，\\&quot;max_connections\\&quot;:\\&quot;10\\&quot;。为空时不修改参数值，key不为空时value也不可为空。 - value：参数值，\\&quot;max_connections\\&quot;:\\&quot;10\\&quot;。
        :type values: dict(str, str)
        """
        self._values = None
        self.discriminator = None
        self.values = values

    @property
    def values(self):
        """Gets the values of this UpdateInstanceConfigurationRequestBody.

        参数值对象，用户基于默认参数模板自定义的参数值。为空时不修改参数值。  - key：参数名称，"max_connections":"10"。为空时不修改参数值，key不为空时value也不可为空。 - value：参数值，"max_connections":"10"。

        :return: The values of this UpdateInstanceConfigurationRequestBody.
        :rtype: dict(str, str)
        """
        return self._values

    @values.setter
    def values(self, values):
        """Sets the values of this UpdateInstanceConfigurationRequestBody.

        参数值对象，用户基于默认参数模板自定义的参数值。为空时不修改参数值。  - key：参数名称，"max_connections":"10"。为空时不修改参数值，key不为空时value也不可为空。 - value：参数值，"max_connections":"10"。

        :param values: The values of this UpdateInstanceConfigurationRequestBody.
        :type values: dict(str, str)
        """
        self._values = values

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
        if not isinstance(other, UpdateInstanceConfigurationRequestBody):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other