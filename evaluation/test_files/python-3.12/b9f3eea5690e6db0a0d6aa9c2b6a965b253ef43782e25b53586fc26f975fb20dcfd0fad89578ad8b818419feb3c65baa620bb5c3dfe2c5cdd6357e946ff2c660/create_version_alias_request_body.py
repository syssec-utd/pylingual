import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class CreateVersionAliasRequestBody:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'name': 'str', 'version': 'str', 'description': 'str', 'additional_version_weights': 'dict(str, int)'}
    attribute_map = {'name': 'name', 'version': 'version', 'description': 'description', 'additional_version_weights': 'additional_version_weights'}

    def __init__(self, name=None, version=None, description=None, additional_version_weights=None):
        """CreateVersionAliasRequestBody

        The model defined in huaweicloud sdk

        :param name: 要获取的别名名称。
        :type name: str
        :param version: 别名对应的版本名称。
        :type version: str
        :param description: 别名描述信息。
        :type description: str
        :param additional_version_weights: 灰度版本信息
        :type additional_version_weights: dict(str, int)
        """
        self._name = None
        self._version = None
        self._description = None
        self._additional_version_weights = None
        self.discriminator = None
        self.name = name
        self.version = version
        if description is not None:
            self.description = description
        if additional_version_weights is not None:
            self.additional_version_weights = additional_version_weights

    @property
    def name(self):
        """Gets the name of this CreateVersionAliasRequestBody.

        要获取的别名名称。

        :return: The name of this CreateVersionAliasRequestBody.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateVersionAliasRequestBody.

        要获取的别名名称。

        :param name: The name of this CreateVersionAliasRequestBody.
        :type name: str
        """
        self._name = name

    @property
    def version(self):
        """Gets the version of this CreateVersionAliasRequestBody.

        别名对应的版本名称。

        :return: The version of this CreateVersionAliasRequestBody.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this CreateVersionAliasRequestBody.

        别名对应的版本名称。

        :param version: The version of this CreateVersionAliasRequestBody.
        :type version: str
        """
        self._version = version

    @property
    def description(self):
        """Gets the description of this CreateVersionAliasRequestBody.

        别名描述信息。

        :return: The description of this CreateVersionAliasRequestBody.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateVersionAliasRequestBody.

        别名描述信息。

        :param description: The description of this CreateVersionAliasRequestBody.
        :type description: str
        """
        self._description = description

    @property
    def additional_version_weights(self):
        """Gets the additional_version_weights of this CreateVersionAliasRequestBody.

        灰度版本信息

        :return: The additional_version_weights of this CreateVersionAliasRequestBody.
        :rtype: dict(str, int)
        """
        return self._additional_version_weights

    @additional_version_weights.setter
    def additional_version_weights(self, additional_version_weights):
        """Sets the additional_version_weights of this CreateVersionAliasRequestBody.

        灰度版本信息

        :param additional_version_weights: The additional_version_weights of this CreateVersionAliasRequestBody.
        :type additional_version_weights: dict(str, int)
        """
        self._additional_version_weights = additional_version_weights

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
        if not isinstance(other, CreateVersionAliasRequestBody):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other