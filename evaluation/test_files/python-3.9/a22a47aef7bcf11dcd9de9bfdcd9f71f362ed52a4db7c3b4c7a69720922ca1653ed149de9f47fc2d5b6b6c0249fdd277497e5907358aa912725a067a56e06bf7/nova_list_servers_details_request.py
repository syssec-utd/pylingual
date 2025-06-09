import re
import six
from g42cloudsdkcore.utils.http_utils import sanitize_for_serialization

class NovaListServersDetailsRequest:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'changes_since': 'str', 'flavor': 'str', 'image': 'str', 'ip': 'str', 'limit': 'int', 'marker': 'str', 'name': 'str', 'not_tags': 'str', 'reservation_id': 'str', 'sort_key': 'str', 'status': 'str', 'tags': 'str', 'open_stack_api_version': 'str'}
    attribute_map = {'changes_since': 'changes-since', 'flavor': 'flavor', 'image': 'image', 'ip': 'ip', 'limit': 'limit', 'marker': 'marker', 'name': 'name', 'not_tags': 'not-tags', 'reservation_id': 'reservation_id', 'sort_key': 'sort_key', 'status': 'status', 'tags': 'tags', 'open_stack_api_version': 'OpenStack-API-Version'}

    def __init__(self, changes_since=None, flavor=None, image=None, ip=None, limit=None, marker=None, name=None, not_tags=None, reservation_id=None, sort_key=None, status=None, tags=None, open_stack_api_version=None):
        """NovaListServersDetailsRequest

        The model defined in g42cloud sdk

        :param changes_since: The param of the NovaListServersDetailsRequest
        :type changes_since: str
        :param flavor: The param of the NovaListServersDetailsRequest
        :type flavor: str
        :param image: The param of the NovaListServersDetailsRequest
        :type image: str
        :param ip: The param of the NovaListServersDetailsRequest
        :type ip: str
        :param limit: The param of the NovaListServersDetailsRequest
        :type limit: int
        :param marker: The param of the NovaListServersDetailsRequest
        :type marker: str
        :param name: The param of the NovaListServersDetailsRequest
        :type name: str
        :param not_tags: The param of the NovaListServersDetailsRequest
        :type not_tags: str
        :param reservation_id: The param of the NovaListServersDetailsRequest
        :type reservation_id: str
        :param sort_key: The param of the NovaListServersDetailsRequest
        :type sort_key: str
        :param status: The param of the NovaListServersDetailsRequest
        :type status: str
        :param tags: The param of the NovaListServersDetailsRequest
        :type tags: str
        :param open_stack_api_version: The param of the NovaListServersDetailsRequest
        :type open_stack_api_version: str
        """
        self._changes_since = None
        self._flavor = None
        self._image = None
        self._ip = None
        self._limit = None
        self._marker = None
        self._name = None
        self._not_tags = None
        self._reservation_id = None
        self._sort_key = None
        self._status = None
        self._tags = None
        self._open_stack_api_version = None
        self.discriminator = None
        if changes_since is not None:
            self.changes_since = changes_since
        if flavor is not None:
            self.flavor = flavor
        if image is not None:
            self.image = image
        if ip is not None:
            self.ip = ip
        if limit is not None:
            self.limit = limit
        if marker is not None:
            self.marker = marker
        if name is not None:
            self.name = name
        if not_tags is not None:
            self.not_tags = not_tags
        if reservation_id is not None:
            self.reservation_id = reservation_id
        if sort_key is not None:
            self.sort_key = sort_key
        if status is not None:
            self.status = status
        if tags is not None:
            self.tags = tags
        if open_stack_api_version is not None:
            self.open_stack_api_version = open_stack_api_version

    @property
    def changes_since(self):
        """Gets the changes_since of this NovaListServersDetailsRequest.

        :return: The changes_since of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._changes_since

    @changes_since.setter
    def changes_since(self, changes_since):
        """Sets the changes_since of this NovaListServersDetailsRequest.

        :param changes_since: The changes_since of this NovaListServersDetailsRequest.
        :type changes_since: str
        """
        self._changes_since = changes_since

    @property
    def flavor(self):
        """Gets the flavor of this NovaListServersDetailsRequest.

        :return: The flavor of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._flavor

    @flavor.setter
    def flavor(self, flavor):
        """Sets the flavor of this NovaListServersDetailsRequest.

        :param flavor: The flavor of this NovaListServersDetailsRequest.
        :type flavor: str
        """
        self._flavor = flavor

    @property
    def image(self):
        """Gets the image of this NovaListServersDetailsRequest.

        :return: The image of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this NovaListServersDetailsRequest.

        :param image: The image of this NovaListServersDetailsRequest.
        :type image: str
        """
        self._image = image

    @property
    def ip(self):
        """Gets the ip of this NovaListServersDetailsRequest.

        :return: The ip of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._ip

    @ip.setter
    def ip(self, ip):
        """Sets the ip of this NovaListServersDetailsRequest.

        :param ip: The ip of this NovaListServersDetailsRequest.
        :type ip: str
        """
        self._ip = ip

    @property
    def limit(self):
        """Gets the limit of this NovaListServersDetailsRequest.

        :return: The limit of this NovaListServersDetailsRequest.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this NovaListServersDetailsRequest.

        :param limit: The limit of this NovaListServersDetailsRequest.
        :type limit: int
        """
        self._limit = limit

    @property
    def marker(self):
        """Gets the marker of this NovaListServersDetailsRequest.

        :return: The marker of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._marker

    @marker.setter
    def marker(self, marker):
        """Sets the marker of this NovaListServersDetailsRequest.

        :param marker: The marker of this NovaListServersDetailsRequest.
        :type marker: str
        """
        self._marker = marker

    @property
    def name(self):
        """Gets the name of this NovaListServersDetailsRequest.

        :return: The name of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NovaListServersDetailsRequest.

        :param name: The name of this NovaListServersDetailsRequest.
        :type name: str
        """
        self._name = name

    @property
    def not_tags(self):
        """Gets the not_tags of this NovaListServersDetailsRequest.

        :return: The not_tags of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._not_tags

    @not_tags.setter
    def not_tags(self, not_tags):
        """Sets the not_tags of this NovaListServersDetailsRequest.

        :param not_tags: The not_tags of this NovaListServersDetailsRequest.
        :type not_tags: str
        """
        self._not_tags = not_tags

    @property
    def reservation_id(self):
        """Gets the reservation_id of this NovaListServersDetailsRequest.

        :return: The reservation_id of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._reservation_id

    @reservation_id.setter
    def reservation_id(self, reservation_id):
        """Sets the reservation_id of this NovaListServersDetailsRequest.

        :param reservation_id: The reservation_id of this NovaListServersDetailsRequest.
        :type reservation_id: str
        """
        self._reservation_id = reservation_id

    @property
    def sort_key(self):
        """Gets the sort_key of this NovaListServersDetailsRequest.

        :return: The sort_key of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._sort_key

    @sort_key.setter
    def sort_key(self, sort_key):
        """Sets the sort_key of this NovaListServersDetailsRequest.

        :param sort_key: The sort_key of this NovaListServersDetailsRequest.
        :type sort_key: str
        """
        self._sort_key = sort_key

    @property
    def status(self):
        """Gets the status of this NovaListServersDetailsRequest.

        :return: The status of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this NovaListServersDetailsRequest.

        :param status: The status of this NovaListServersDetailsRequest.
        :type status: str
        """
        self._status = status

    @property
    def tags(self):
        """Gets the tags of this NovaListServersDetailsRequest.

        :return: The tags of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this NovaListServersDetailsRequest.

        :param tags: The tags of this NovaListServersDetailsRequest.
        :type tags: str
        """
        self._tags = tags

    @property
    def open_stack_api_version(self):
        """Gets the open_stack_api_version of this NovaListServersDetailsRequest.

        :return: The open_stack_api_version of this NovaListServersDetailsRequest.
        :rtype: str
        """
        return self._open_stack_api_version

    @open_stack_api_version.setter
    def open_stack_api_version(self, open_stack_api_version):
        """Sets the open_stack_api_version of this NovaListServersDetailsRequest.

        :param open_stack_api_version: The open_stack_api_version of this NovaListServersDetailsRequest.
        :type open_stack_api_version: str
        """
        self._open_stack_api_version = open_stack_api_version

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
        if not isinstance(other, NovaListServersDetailsRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other