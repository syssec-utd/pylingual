import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class MemberGroupInfo:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'member_group_name': 'str', 'member_group_remark': 'str', 'member_group_weight': 'int', 'dict_code': 'str', 'member_group_id': 'str', 'create_time': 'datetime', 'update_time': 'datetime'}
    attribute_map = {'member_group_name': 'member_group_name', 'member_group_remark': 'member_group_remark', 'member_group_weight': 'member_group_weight', 'dict_code': 'dict_code', 'member_group_id': 'member_group_id', 'create_time': 'create_time', 'update_time': 'update_time'}

    def __init__(self, member_group_name=None, member_group_remark=None, member_group_weight=None, dict_code=None, member_group_id=None, create_time=None, update_time=None):
        """MemberGroupInfo

        The model defined in huaweicloud sdk

        :param member_group_name: VPC通道后端服务器组名称
        :type member_group_name: str
        :param member_group_remark: VPC通道后端服务器组描述
        :type member_group_remark: str
        :param member_group_weight: VPC通道后端服务器组权重值。  当前服务器组存在服务器且此权重值存在时，自动使用此权重值分配权重。
        :type member_group_weight: int
        :param dict_code: VPC通道后端服务器组的字典编码  支持英文，数字，特殊字符（-_.）  暂不支持
        :type dict_code: str
        :param member_group_id: VPC通道后端服务器组编号
        :type member_group_id: str
        :param create_time: VPC通道后端服务器组创建时间
        :type create_time: datetime
        :param update_time: VPC通道后端服务器组更新时间
        :type update_time: datetime
        """
        self._member_group_name = None
        self._member_group_remark = None
        self._member_group_weight = None
        self._dict_code = None
        self._member_group_id = None
        self._create_time = None
        self._update_time = None
        self.discriminator = None
        self.member_group_name = member_group_name
        if member_group_remark is not None:
            self.member_group_remark = member_group_remark
        if member_group_weight is not None:
            self.member_group_weight = member_group_weight
        if dict_code is not None:
            self.dict_code = dict_code
        if member_group_id is not None:
            self.member_group_id = member_group_id
        if create_time is not None:
            self.create_time = create_time
        if update_time is not None:
            self.update_time = update_time

    @property
    def member_group_name(self):
        """Gets the member_group_name of this MemberGroupInfo.

        VPC通道后端服务器组名称

        :return: The member_group_name of this MemberGroupInfo.
        :rtype: str
        """
        return self._member_group_name

    @member_group_name.setter
    def member_group_name(self, member_group_name):
        """Sets the member_group_name of this MemberGroupInfo.

        VPC通道后端服务器组名称

        :param member_group_name: The member_group_name of this MemberGroupInfo.
        :type member_group_name: str
        """
        self._member_group_name = member_group_name

    @property
    def member_group_remark(self):
        """Gets the member_group_remark of this MemberGroupInfo.

        VPC通道后端服务器组描述

        :return: The member_group_remark of this MemberGroupInfo.
        :rtype: str
        """
        return self._member_group_remark

    @member_group_remark.setter
    def member_group_remark(self, member_group_remark):
        """Sets the member_group_remark of this MemberGroupInfo.

        VPC通道后端服务器组描述

        :param member_group_remark: The member_group_remark of this MemberGroupInfo.
        :type member_group_remark: str
        """
        self._member_group_remark = member_group_remark

    @property
    def member_group_weight(self):
        """Gets the member_group_weight of this MemberGroupInfo.

        VPC通道后端服务器组权重值。  当前服务器组存在服务器且此权重值存在时，自动使用此权重值分配权重。

        :return: The member_group_weight of this MemberGroupInfo.
        :rtype: int
        """
        return self._member_group_weight

    @member_group_weight.setter
    def member_group_weight(self, member_group_weight):
        """Sets the member_group_weight of this MemberGroupInfo.

        VPC通道后端服务器组权重值。  当前服务器组存在服务器且此权重值存在时，自动使用此权重值分配权重。

        :param member_group_weight: The member_group_weight of this MemberGroupInfo.
        :type member_group_weight: int
        """
        self._member_group_weight = member_group_weight

    @property
    def dict_code(self):
        """Gets the dict_code of this MemberGroupInfo.

        VPC通道后端服务器组的字典编码  支持英文，数字，特殊字符（-_.）  暂不支持

        :return: The dict_code of this MemberGroupInfo.
        :rtype: str
        """
        return self._dict_code

    @dict_code.setter
    def dict_code(self, dict_code):
        """Sets the dict_code of this MemberGroupInfo.

        VPC通道后端服务器组的字典编码  支持英文，数字，特殊字符（-_.）  暂不支持

        :param dict_code: The dict_code of this MemberGroupInfo.
        :type dict_code: str
        """
        self._dict_code = dict_code

    @property
    def member_group_id(self):
        """Gets the member_group_id of this MemberGroupInfo.

        VPC通道后端服务器组编号

        :return: The member_group_id of this MemberGroupInfo.
        :rtype: str
        """
        return self._member_group_id

    @member_group_id.setter
    def member_group_id(self, member_group_id):
        """Sets the member_group_id of this MemberGroupInfo.

        VPC通道后端服务器组编号

        :param member_group_id: The member_group_id of this MemberGroupInfo.
        :type member_group_id: str
        """
        self._member_group_id = member_group_id

    @property
    def create_time(self):
        """Gets the create_time of this MemberGroupInfo.

        VPC通道后端服务器组创建时间

        :return: The create_time of this MemberGroupInfo.
        :rtype: datetime
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this MemberGroupInfo.

        VPC通道后端服务器组创建时间

        :param create_time: The create_time of this MemberGroupInfo.
        :type create_time: datetime
        """
        self._create_time = create_time

    @property
    def update_time(self):
        """Gets the update_time of this MemberGroupInfo.

        VPC通道后端服务器组更新时间

        :return: The update_time of this MemberGroupInfo.
        :rtype: datetime
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this MemberGroupInfo.

        VPC通道后端服务器组更新时间

        :param update_time: The update_time of this MemberGroupInfo.
        :type update_time: datetime
        """
        self._update_time = update_time

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
        if not isinstance(other, MemberGroupInfo):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other