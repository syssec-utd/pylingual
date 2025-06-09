import re
import six
from g42cloudsdkcore.utils.http_utils import sanitize_for_serialization

class ListImageTagsRequest:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'image_id': 'str'}
    attribute_map = {'image_id': 'image_id'}

    def __init__(self, image_id=None):
        """ListImageTagsRequest

        The model defined in g42cloud sdk

        :param image_id: The param of the ListImageTagsRequest
        :type image_id: str
        """
        self._image_id = None
        self.discriminator = None
        self.image_id = image_id

    @property
    def image_id(self):
        """Gets the image_id of this ListImageTagsRequest.

        :return: The image_id of this ListImageTagsRequest.
        :rtype: str
        """
        return self._image_id

    @image_id.setter
    def image_id(self, image_id):
        """Sets the image_id of this ListImageTagsRequest.

        :param image_id: The image_id of this ListImageTagsRequest.
        :type image_id: str
        """
        self._image_id = image_id

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
        if not isinstance(other, ListImageTagsRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other