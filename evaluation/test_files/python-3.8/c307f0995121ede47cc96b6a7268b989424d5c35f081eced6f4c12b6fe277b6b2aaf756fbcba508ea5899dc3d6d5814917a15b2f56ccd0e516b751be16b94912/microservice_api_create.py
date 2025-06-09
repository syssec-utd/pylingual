import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class MicroserviceApiCreate:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'name': 'str', 'req_method': 'str', 'req_uri': 'str', 'match_mode': 'str'}
    attribute_map = {'name': 'name', 'req_method': 'req_method', 'req_uri': 'req_uri', 'match_mode': 'match_mode'}

    def __init__(self, name=None, req_method=None, req_uri=None, match_mode=None):
        """MicroserviceApiCreate

        The model defined in huaweicloud sdk

        :param name: API名称。  支持汉字、英文、数字、中划线、下划线、点、斜杠、中英文格式下的小括号和冒号、中文格式下的顿号，且只能以英文、汉字和数字开头。 &gt; 中文字符必须为UTF-8或者unicode编码。
        :type name: str
        :param req_method: API的请求方式
        :type req_method: str
        :param req_uri: 请求地址。可以包含请求参数，用{}标识，比如/getUserInfo/{userId}，支持 * % - _ . 等特殊字符，总长度不超过512，且满足URI规范。 /apic/health_check为服务集成预置的健康检查路径，当req_method&#x3D;GET时不支持req_uri&#x3D;/apic/health_check。 &gt; 需要服从URI规范。
        :type req_uri: str
        :param match_mode: API的匹配方式 - SWA：前缀匹配 - NORMAL：正常匹配（绝对匹配） 默认：NORMAL
        :type match_mode: str
        """
        self._name = None
        self._req_method = None
        self._req_uri = None
        self._match_mode = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if req_method is not None:
            self.req_method = req_method
        self.req_uri = req_uri
        if match_mode is not None:
            self.match_mode = match_mode

    @property
    def name(self):
        """Gets the name of this MicroserviceApiCreate.

        API名称。  支持汉字、英文、数字、中划线、下划线、点、斜杠、中英文格式下的小括号和冒号、中文格式下的顿号，且只能以英文、汉字和数字开头。 > 中文字符必须为UTF-8或者unicode编码。

        :return: The name of this MicroserviceApiCreate.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MicroserviceApiCreate.

        API名称。  支持汉字、英文、数字、中划线、下划线、点、斜杠、中英文格式下的小括号和冒号、中文格式下的顿号，且只能以英文、汉字和数字开头。 > 中文字符必须为UTF-8或者unicode编码。

        :param name: The name of this MicroserviceApiCreate.
        :type name: str
        """
        self._name = name

    @property
    def req_method(self):
        """Gets the req_method of this MicroserviceApiCreate.

        API的请求方式

        :return: The req_method of this MicroserviceApiCreate.
        :rtype: str
        """
        return self._req_method

    @req_method.setter
    def req_method(self, req_method):
        """Sets the req_method of this MicroserviceApiCreate.

        API的请求方式

        :param req_method: The req_method of this MicroserviceApiCreate.
        :type req_method: str
        """
        self._req_method = req_method

    @property
    def req_uri(self):
        """Gets the req_uri of this MicroserviceApiCreate.

        请求地址。可以包含请求参数，用{}标识，比如/getUserInfo/{userId}，支持 * % - _ . 等特殊字符，总长度不超过512，且满足URI规范。 /apic/health_check为服务集成预置的健康检查路径，当req_method=GET时不支持req_uri=/apic/health_check。 > 需要服从URI规范。

        :return: The req_uri of this MicroserviceApiCreate.
        :rtype: str
        """
        return self._req_uri

    @req_uri.setter
    def req_uri(self, req_uri):
        """Sets the req_uri of this MicroserviceApiCreate.

        请求地址。可以包含请求参数，用{}标识，比如/getUserInfo/{userId}，支持 * % - _ . 等特殊字符，总长度不超过512，且满足URI规范。 /apic/health_check为服务集成预置的健康检查路径，当req_method=GET时不支持req_uri=/apic/health_check。 > 需要服从URI规范。

        :param req_uri: The req_uri of this MicroserviceApiCreate.
        :type req_uri: str
        """
        self._req_uri = req_uri

    @property
    def match_mode(self):
        """Gets the match_mode of this MicroserviceApiCreate.

        API的匹配方式 - SWA：前缀匹配 - NORMAL：正常匹配（绝对匹配） 默认：NORMAL

        :return: The match_mode of this MicroserviceApiCreate.
        :rtype: str
        """
        return self._match_mode

    @match_mode.setter
    def match_mode(self, match_mode):
        """Sets the match_mode of this MicroserviceApiCreate.

        API的匹配方式 - SWA：前缀匹配 - NORMAL：正常匹配（绝对匹配） 默认：NORMAL

        :param match_mode: The match_mode of this MicroserviceApiCreate.
        :type match_mode: str
        """
        self._match_mode = match_mode

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
        if not isinstance(other, MicroserviceApiCreate):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other