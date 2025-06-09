import re
import six
from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class CreateApiAclBindingV2Response(SdkResponse):
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'acl_bindings': 'list[AclApiBindingInfo]'}
    attribute_map = {'acl_bindings': 'acl_bindings'}

    def __init__(self, acl_bindings=None):
        """CreateApiAclBindingV2Response

        The model defined in huaweicloud sdk

        :param acl_bindings: API与ACL的绑定关系列表
        :type acl_bindings: list[:class:`huaweicloudsdkroma.v2.AclApiBindingInfo`]
        """
        super(CreateApiAclBindingV2Response, self).__init__()
        self._acl_bindings = None
        self.discriminator = None
        if acl_bindings is not None:
            self.acl_bindings = acl_bindings

    @property
    def acl_bindings(self):
        """Gets the acl_bindings of this CreateApiAclBindingV2Response.

        API与ACL的绑定关系列表

        :return: The acl_bindings of this CreateApiAclBindingV2Response.
        :rtype: list[:class:`huaweicloudsdkroma.v2.AclApiBindingInfo`]
        """
        return self._acl_bindings

    @acl_bindings.setter
    def acl_bindings(self, acl_bindings):
        """Sets the acl_bindings of this CreateApiAclBindingV2Response.

        API与ACL的绑定关系列表

        :param acl_bindings: The acl_bindings of this CreateApiAclBindingV2Response.
        :type acl_bindings: list[:class:`huaweicloudsdkroma.v2.AclApiBindingInfo`]
        """
        self._acl_bindings = acl_bindings

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
        if not isinstance(other, CreateApiAclBindingV2Response):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other