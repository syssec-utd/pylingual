import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class CreateLocation:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'name': 'str', 'province': 'str', 'city': 'str', 'district': 'str', 'country': 'str', 'condition': 'Condition', 'description': 'str'}
    attribute_map = {'name': 'name', 'province': 'province', 'city': 'city', 'district': 'district', 'country': 'country', 'condition': 'condition', 'description': 'description'}

    def __init__(self, name=None, province=None, city=None, district=None, country=None, condition=None, description=None):
        """CreateLocation

        The model defined in huaweicloud sdk

        :param name: 场地名称，最大支持长度为64个字节。只包含中文字符、英文字母（a-z、A-Z）、数字（0-9）、下划线（_）、中划线（-）
        :type name: str
        :param province: 场地所在省/自治区/直辖市
        :type province: str
        :param city: 场地所在市/区
        :type city: str
        :param district: 场地所在区/县
        :type district: str
        :param country: 场地所在国家
        :type country: str
        :param condition: 
        :type condition: :class:`huaweicloudsdkies.v1.Condition`
        :param description: 场地描述，最大支持长度为255个字节，不允许包含&lt;&gt;
        :type description: str
        """
        self._name = None
        self._province = None
        self._city = None
        self._district = None
        self._country = None
        self._condition = None
        self._description = None
        self.discriminator = None
        self.name = name
        self.province = province
        self.city = city
        self.district = district
        if country is not None:
            self.country = country
        self.condition = condition
        if description is not None:
            self.description = description

    @property
    def name(self):
        """Gets the name of this CreateLocation.

        场地名称，最大支持长度为64个字节。只包含中文字符、英文字母（a-z、A-Z）、数字（0-9）、下划线（_）、中划线（-）

        :return: The name of this CreateLocation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateLocation.

        场地名称，最大支持长度为64个字节。只包含中文字符、英文字母（a-z、A-Z）、数字（0-9）、下划线（_）、中划线（-）

        :param name: The name of this CreateLocation.
        :type name: str
        """
        self._name = name

    @property
    def province(self):
        """Gets the province of this CreateLocation.

        场地所在省/自治区/直辖市

        :return: The province of this CreateLocation.
        :rtype: str
        """
        return self._province

    @province.setter
    def province(self, province):
        """Sets the province of this CreateLocation.

        场地所在省/自治区/直辖市

        :param province: The province of this CreateLocation.
        :type province: str
        """
        self._province = province

    @property
    def city(self):
        """Gets the city of this CreateLocation.

        场地所在市/区

        :return: The city of this CreateLocation.
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this CreateLocation.

        场地所在市/区

        :param city: The city of this CreateLocation.
        :type city: str
        """
        self._city = city

    @property
    def district(self):
        """Gets the district of this CreateLocation.

        场地所在区/县

        :return: The district of this CreateLocation.
        :rtype: str
        """
        return self._district

    @district.setter
    def district(self, district):
        """Sets the district of this CreateLocation.

        场地所在区/县

        :param district: The district of this CreateLocation.
        :type district: str
        """
        self._district = district

    @property
    def country(self):
        """Gets the country of this CreateLocation.

        场地所在国家

        :return: The country of this CreateLocation.
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this CreateLocation.

        场地所在国家

        :param country: The country of this CreateLocation.
        :type country: str
        """
        self._country = country

    @property
    def condition(self):
        """Gets the condition of this CreateLocation.


        :return: The condition of this CreateLocation.
        :rtype: :class:`huaweicloudsdkies.v1.Condition`
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """Sets the condition of this CreateLocation.


        :param condition: The condition of this CreateLocation.
        :type condition: :class:`huaweicloudsdkies.v1.Condition`
        """
        self._condition = condition

    @property
    def description(self):
        """Gets the description of this CreateLocation.

        场地描述，最大支持长度为255个字节，不允许包含<>

        :return: The description of this CreateLocation.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateLocation.

        场地描述，最大支持长度为255个字节，不允许包含<>

        :param description: The description of this CreateLocation.
        :type description: str
        """
        self._description = description

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
        if not isinstance(other, CreateLocation):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other