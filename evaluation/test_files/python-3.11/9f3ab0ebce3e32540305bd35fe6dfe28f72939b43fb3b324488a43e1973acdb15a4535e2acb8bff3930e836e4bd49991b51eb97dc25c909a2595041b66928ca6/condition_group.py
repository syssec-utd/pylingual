import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class ConditionGroup:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'conditions': 'list[RuleCondition]', 'logic': 'str', 'time_range': 'TimeRange'}
    attribute_map = {'conditions': 'conditions', 'logic': 'logic', 'time_range': 'time_range'}

    def __init__(self, conditions=None, logic=None, time_range=None):
        """ConditionGroup

        The model defined in huaweicloud sdk

        :param conditions: **参数说明**：规则的条件列表，单个规则最多支持设置10个条件。
        :type conditions: list[:class:`huaweicloudsdkiotda.v5.RuleCondition`]
        :param logic: **参数说明**：规则条件列表中多个条件之间的逻辑关系，默认值：and。 **取值范围**： - and：逻辑且。 - or：逻辑或。
        :type logic: str
        :param time_range: 
        :type time_range: :class:`huaweicloudsdkiotda.v5.TimeRange`
        """
        self._conditions = None
        self._logic = None
        self._time_range = None
        self.discriminator = None
        if conditions is not None:
            self.conditions = conditions
        if logic is not None:
            self.logic = logic
        if time_range is not None:
            self.time_range = time_range

    @property
    def conditions(self):
        """Gets the conditions of this ConditionGroup.

        **参数说明**：规则的条件列表，单个规则最多支持设置10个条件。

        :return: The conditions of this ConditionGroup.
        :rtype: list[:class:`huaweicloudsdkiotda.v5.RuleCondition`]
        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        """Sets the conditions of this ConditionGroup.

        **参数说明**：规则的条件列表，单个规则最多支持设置10个条件。

        :param conditions: The conditions of this ConditionGroup.
        :type conditions: list[:class:`huaweicloudsdkiotda.v5.RuleCondition`]
        """
        self._conditions = conditions

    @property
    def logic(self):
        """Gets the logic of this ConditionGroup.

        **参数说明**：规则条件列表中多个条件之间的逻辑关系，默认值：and。 **取值范围**： - and：逻辑且。 - or：逻辑或。

        :return: The logic of this ConditionGroup.
        :rtype: str
        """
        return self._logic

    @logic.setter
    def logic(self, logic):
        """Sets the logic of this ConditionGroup.

        **参数说明**：规则条件列表中多个条件之间的逻辑关系，默认值：and。 **取值范围**： - and：逻辑且。 - or：逻辑或。

        :param logic: The logic of this ConditionGroup.
        :type logic: str
        """
        self._logic = logic

    @property
    def time_range(self):
        """Gets the time_range of this ConditionGroup.


        :return: The time_range of this ConditionGroup.
        :rtype: :class:`huaweicloudsdkiotda.v5.TimeRange`
        """
        return self._time_range

    @time_range.setter
    def time_range(self, time_range):
        """Sets the time_range of this ConditionGroup.


        :param time_range: The time_range of this ConditionGroup.
        :type time_range: :class:`huaweicloudsdkiotda.v5.TimeRange`
        """
        self._time_range = time_range

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
        if not isinstance(other, ConditionGroup):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other