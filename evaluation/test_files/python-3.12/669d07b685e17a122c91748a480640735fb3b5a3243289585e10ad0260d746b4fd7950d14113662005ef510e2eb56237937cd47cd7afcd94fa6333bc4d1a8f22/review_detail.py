import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class ReviewDetail:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'confidence': 'str', 'label': 'str'}
    attribute_map = {'confidence': 'confidence', 'label': 'label'}

    def __init__(self, confidence=None, label=None):
        """ReviewDetail

        The model defined in huaweicloud sdk

        :param confidence: 置信度。  取值范围：[0,1]。
        :type confidence: str
        :param label: 每个检测结果的标签化说明。 - politics场景：label为对应的政治人物信息。 - terrorism场景： label为对应的暴恐元素（枪支、刀具、火灾等） 信息。 - porn场景：label为对应的涉黄元素（涉黄、性感等）信息。
        :type label: str
        """
        self._confidence = None
        self._label = None
        self.discriminator = None
        self.confidence = confidence
        if label is not None:
            self.label = label

    @property
    def confidence(self):
        """Gets the confidence of this ReviewDetail.

        置信度。  取值范围：[0,1]。

        :return: The confidence of this ReviewDetail.
        :rtype: str
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        """Sets the confidence of this ReviewDetail.

        置信度。  取值范围：[0,1]。

        :param confidence: The confidence of this ReviewDetail.
        :type confidence: str
        """
        self._confidence = confidence

    @property
    def label(self):
        """Gets the label of this ReviewDetail.

        每个检测结果的标签化说明。 - politics场景：label为对应的政治人物信息。 - terrorism场景： label为对应的暴恐元素（枪支、刀具、火灾等） 信息。 - porn场景：label为对应的涉黄元素（涉黄、性感等）信息。

        :return: The label of this ReviewDetail.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this ReviewDetail.

        每个检测结果的标签化说明。 - politics场景：label为对应的政治人物信息。 - terrorism场景： label为对应的暴恐元素（枪支、刀具、火灾等） 信息。 - porn场景：label为对应的涉黄元素（涉黄、性感等）信息。

        :param label: The label of this ReviewDetail.
        :type label: str
        """
        self._label = label

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
        if not isinstance(other, ReviewDetail):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other