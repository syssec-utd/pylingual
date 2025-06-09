import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class ModResourceDTO:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'id': 'str', 'type': 'str', 'expire_date': 'int', 'is_disabled': 'bool'}
    attribute_map = {'id': 'id', 'type': 'type', 'expire_date': 'expireDate', 'is_disabled': 'isDisabled'}

    def __init__(self, id=None, type=None, expire_date=None, is_disabled=None):
        """ModResourceDTO

        The model defined in huaweicloud sdk

        :param id: 资源标识
        :type id: str
        :param type: 资源类型，企业内ID和TYPE唯一标识一个资源项，若只传资源ID可能会修改多个资源的信息. - VMR        - 云会议室 - CONF_CALL  - 会议并发数 - HARD_1080P - 1080P硬终端 - HARD_720P  - 720P硬终端 - SOFT       - 软终端用户数 - ROOM       - 大屏软终端 - LIVE       - 直播推流 - RECORD     - 录播空间 - HARD_THIRD_PARTY - 第三方硬终端账号 - HUAWEI_VISION -智慧屏
        :type type: str
        :param expire_date: 到期时间
        :type expire_date: int
        :param is_disabled: 资源是否被停用
        :type is_disabled: bool
        """
        self._id = None
        self._type = None
        self._expire_date = None
        self._is_disabled = None
        self.discriminator = None
        self.id = id
        if type is not None:
            self.type = type
        if expire_date is not None:
            self.expire_date = expire_date
        if is_disabled is not None:
            self.is_disabled = is_disabled

    @property
    def id(self):
        """Gets the id of this ModResourceDTO.

        资源标识

        :return: The id of this ModResourceDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModResourceDTO.

        资源标识

        :param id: The id of this ModResourceDTO.
        :type id: str
        """
        self._id = id

    @property
    def type(self):
        """Gets the type of this ModResourceDTO.

        资源类型，企业内ID和TYPE唯一标识一个资源项，若只传资源ID可能会修改多个资源的信息. - VMR        - 云会议室 - CONF_CALL  - 会议并发数 - HARD_1080P - 1080P硬终端 - HARD_720P  - 720P硬终端 - SOFT       - 软终端用户数 - ROOM       - 大屏软终端 - LIVE       - 直播推流 - RECORD     - 录播空间 - HARD_THIRD_PARTY - 第三方硬终端账号 - HUAWEI_VISION -智慧屏

        :return: The type of this ModResourceDTO.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ModResourceDTO.

        资源类型，企业内ID和TYPE唯一标识一个资源项，若只传资源ID可能会修改多个资源的信息. - VMR        - 云会议室 - CONF_CALL  - 会议并发数 - HARD_1080P - 1080P硬终端 - HARD_720P  - 720P硬终端 - SOFT       - 软终端用户数 - ROOM       - 大屏软终端 - LIVE       - 直播推流 - RECORD     - 录播空间 - HARD_THIRD_PARTY - 第三方硬终端账号 - HUAWEI_VISION -智慧屏

        :param type: The type of this ModResourceDTO.
        :type type: str
        """
        self._type = type

    @property
    def expire_date(self):
        """Gets the expire_date of this ModResourceDTO.

        到期时间

        :return: The expire_date of this ModResourceDTO.
        :rtype: int
        """
        return self._expire_date

    @expire_date.setter
    def expire_date(self, expire_date):
        """Sets the expire_date of this ModResourceDTO.

        到期时间

        :param expire_date: The expire_date of this ModResourceDTO.
        :type expire_date: int
        """
        self._expire_date = expire_date

    @property
    def is_disabled(self):
        """Gets the is_disabled of this ModResourceDTO.

        资源是否被停用

        :return: The is_disabled of this ModResourceDTO.
        :rtype: bool
        """
        return self._is_disabled

    @is_disabled.setter
    def is_disabled(self, is_disabled):
        """Sets the is_disabled of this ModResourceDTO.

        资源是否被停用

        :param is_disabled: The is_disabled of this ModResourceDTO.
        :type is_disabled: bool
        """
        self._is_disabled = is_disabled

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
        if not isinstance(other, ModResourceDTO):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other