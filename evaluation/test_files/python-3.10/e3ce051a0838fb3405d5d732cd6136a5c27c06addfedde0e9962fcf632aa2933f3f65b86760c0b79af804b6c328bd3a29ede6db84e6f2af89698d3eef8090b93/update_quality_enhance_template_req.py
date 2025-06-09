import re
import six
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class UpdateQualityEnhanceTemplateReq:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'template_id': 'int', 'template': 'QualityEnhanceTemplate'}
    attribute_map = {'template_id': 'template_id', 'template': 'template'}

    def __init__(self, template_id=None, template=None):
        """UpdateQualityEnhanceTemplateReq

        The model defined in huaweicloud sdk

        :param template_id: 模板ID。 
        :type template_id: int
        :param template: 
        :type template: :class:`huaweicloudsdkmpc.v1.QualityEnhanceTemplate`
        """
        self._template_id = None
        self._template = None
        self.discriminator = None
        if template_id is not None:
            self.template_id = template_id
        if template is not None:
            self.template = template

    @property
    def template_id(self):
        """Gets the template_id of this UpdateQualityEnhanceTemplateReq.

        模板ID。 

        :return: The template_id of this UpdateQualityEnhanceTemplateReq.
        :rtype: int
        """
        return self._template_id

    @template_id.setter
    def template_id(self, template_id):
        """Sets the template_id of this UpdateQualityEnhanceTemplateReq.

        模板ID。 

        :param template_id: The template_id of this UpdateQualityEnhanceTemplateReq.
        :type template_id: int
        """
        self._template_id = template_id

    @property
    def template(self):
        """Gets the template of this UpdateQualityEnhanceTemplateReq.


        :return: The template of this UpdateQualityEnhanceTemplateReq.
        :rtype: :class:`huaweicloudsdkmpc.v1.QualityEnhanceTemplate`
        """
        return self._template

    @template.setter
    def template(self, template):
        """Sets the template of this UpdateQualityEnhanceTemplateReq.


        :param template: The template of this UpdateQualityEnhanceTemplateReq.
        :type template: :class:`huaweicloudsdkmpc.v1.QualityEnhanceTemplate`
        """
        self._template = template

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
        if not isinstance(other, UpdateQualityEnhanceTemplateReq):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other