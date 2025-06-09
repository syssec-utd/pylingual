import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class NeutronDeleteFirewallGroupRequest:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'firewall_group_id': 'str'}
    attribute_map = {'firewall_group_id': 'firewall_group_id'}

    def __init__(self, firewall_group_id=None):
        """NeutronDeleteFirewallGroupRequest

        The model defined in huaweicloud sdk

        :param firewall_group_id: 网络ACL防火墙组ID
        :type firewall_group_id: str
        """
        self._firewall_group_id = None
        self.discriminator = None
        self.firewall_group_id = firewall_group_id

    @property
    def firewall_group_id(self):
        """Gets the firewall_group_id of this NeutronDeleteFirewallGroupRequest.

        网络ACL防火墙组ID

        :return: The firewall_group_id of this NeutronDeleteFirewallGroupRequest.
        :rtype: str
        """
        return self._firewall_group_id

    @firewall_group_id.setter
    def firewall_group_id(self, firewall_group_id):
        """Sets the firewall_group_id of this NeutronDeleteFirewallGroupRequest.

        网络ACL防火墙组ID

        :param firewall_group_id: The firewall_group_id of this NeutronDeleteFirewallGroupRequest.
        :type firewall_group_id: str
        """
        self._firewall_group_id = firewall_group_id

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
        if not isinstance(other, NeutronDeleteFirewallGroupRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other