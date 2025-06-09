import re
import six
from g42cloudsdkcore.utils.http_utils import sanitize_for_serialization

class ShowVpcPeeringRequest:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'peering_id': 'str'}
    attribute_map = {'peering_id': 'peering_id'}

    def __init__(self, peering_id=None):
        """ShowVpcPeeringRequest

        The model defined in g42cloud sdk

        :param peering_id: The param of the ShowVpcPeeringRequest
        :type peering_id: str
        """
        self._peering_id = None
        self.discriminator = None
        self.peering_id = peering_id

    @property
    def peering_id(self):
        """Gets the peering_id of this ShowVpcPeeringRequest.

        :return: The peering_id of this ShowVpcPeeringRequest.
        :rtype: str
        """
        return self._peering_id

    @peering_id.setter
    def peering_id(self, peering_id):
        """Sets the peering_id of this ShowVpcPeeringRequest.

        :param peering_id: The peering_id of this ShowVpcPeeringRequest.
        :type peering_id: str
        """
        self._peering_id = peering_id

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
        if not isinstance(other, ShowVpcPeeringRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other