import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class ListApisBindedToRequestThrottlingPolicyV2Request:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'instance_id': 'str', 'offset': 'int', 'limit': 'int', 'throttle_id': 'str', 'env_id': 'str', 'group_id': 'str', 'api_id': 'str', 'api_name': 'str'}
    attribute_map = {'instance_id': 'instance_id', 'offset': 'offset', 'limit': 'limit', 'throttle_id': 'throttle_id', 'env_id': 'env_id', 'group_id': 'group_id', 'api_id': 'api_id', 'api_name': 'api_name'}

    def __init__(self, instance_id=None, offset=None, limit=None, throttle_id=None, env_id=None, group_id=None, api_id=None, api_name=None):
        """ListApisBindedToRequestThrottlingPolicyV2Request

        The model defined in huaweicloud sdk

        :param instance_id: 实例ID
        :type instance_id: str
        :param offset: 偏移量，表示从此偏移量开始查询，偏移量小于0时，自动转换为0
        :type offset: int
        :param limit: 每页显示的条目数量
        :type limit: int
        :param throttle_id: 流控策略编号
        :type throttle_id: str
        :param env_id: 环境的ID
        :type env_id: str
        :param group_id: API分组编号
        :type group_id: str
        :param api_id: API编号
        :type api_id: str
        :param api_name: API名称
        :type api_name: str
        """
        self._instance_id = None
        self._offset = None
        self._limit = None
        self._throttle_id = None
        self._env_id = None
        self._group_id = None
        self._api_id = None
        self._api_name = None
        self.discriminator = None
        self.instance_id = instance_id
        if offset is not None:
            self.offset = offset
        if limit is not None:
            self.limit = limit
        self.throttle_id = throttle_id
        if env_id is not None:
            self.env_id = env_id
        if group_id is not None:
            self.group_id = group_id
        if api_id is not None:
            self.api_id = api_id
        if api_name is not None:
            self.api_name = api_name

    @property
    def instance_id(self):
        """Gets the instance_id of this ListApisBindedToRequestThrottlingPolicyV2Request.

        实例ID

        :return: The instance_id of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ListApisBindedToRequestThrottlingPolicyV2Request.

        实例ID

        :param instance_id: The instance_id of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :type instance_id: str
        """
        self._instance_id = instance_id

    @property
    def offset(self):
        """Gets the offset of this ListApisBindedToRequestThrottlingPolicyV2Request.

        偏移量，表示从此偏移量开始查询，偏移量小于0时，自动转换为0

        :return: The offset of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this ListApisBindedToRequestThrottlingPolicyV2Request.

        偏移量，表示从此偏移量开始查询，偏移量小于0时，自动转换为0

        :param offset: The offset of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :type offset: int
        """
        self._offset = offset

    @property
    def limit(self):
        """Gets the limit of this ListApisBindedToRequestThrottlingPolicyV2Request.

        每页显示的条目数量

        :return: The limit of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListApisBindedToRequestThrottlingPolicyV2Request.

        每页显示的条目数量

        :param limit: The limit of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :type limit: int
        """
        self._limit = limit

    @property
    def throttle_id(self):
        """Gets the throttle_id of this ListApisBindedToRequestThrottlingPolicyV2Request.

        流控策略编号

        :return: The throttle_id of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :rtype: str
        """
        return self._throttle_id

    @throttle_id.setter
    def throttle_id(self, throttle_id):
        """Sets the throttle_id of this ListApisBindedToRequestThrottlingPolicyV2Request.

        流控策略编号

        :param throttle_id: The throttle_id of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :type throttle_id: str
        """
        self._throttle_id = throttle_id

    @property
    def env_id(self):
        """Gets the env_id of this ListApisBindedToRequestThrottlingPolicyV2Request.

        环境的ID

        :return: The env_id of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :rtype: str
        """
        return self._env_id

    @env_id.setter
    def env_id(self, env_id):
        """Sets the env_id of this ListApisBindedToRequestThrottlingPolicyV2Request.

        环境的ID

        :param env_id: The env_id of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :type env_id: str
        """
        self._env_id = env_id

    @property
    def group_id(self):
        """Gets the group_id of this ListApisBindedToRequestThrottlingPolicyV2Request.

        API分组编号

        :return: The group_id of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """Sets the group_id of this ListApisBindedToRequestThrottlingPolicyV2Request.

        API分组编号

        :param group_id: The group_id of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :type group_id: str
        """
        self._group_id = group_id

    @property
    def api_id(self):
        """Gets the api_id of this ListApisBindedToRequestThrottlingPolicyV2Request.

        API编号

        :return: The api_id of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :rtype: str
        """
        return self._api_id

    @api_id.setter
    def api_id(self, api_id):
        """Sets the api_id of this ListApisBindedToRequestThrottlingPolicyV2Request.

        API编号

        :param api_id: The api_id of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :type api_id: str
        """
        self._api_id = api_id

    @property
    def api_name(self):
        """Gets the api_name of this ListApisBindedToRequestThrottlingPolicyV2Request.

        API名称

        :return: The api_name of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :rtype: str
        """
        return self._api_name

    @api_name.setter
    def api_name(self, api_name):
        """Sets the api_name of this ListApisBindedToRequestThrottlingPolicyV2Request.

        API名称

        :param api_name: The api_name of this ListApisBindedToRequestThrottlingPolicyV2Request.
        :type api_name: str
        """
        self._api_name = api_name

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
        if not isinstance(other, ListApisBindedToRequestThrottlingPolicyV2Request):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other