import re
import six
from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class ListExtendsParamsResponse(SdkResponse):
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'extends_params': 'list[ExtendsParamV2]', 'common_params': 'list[CommonParamV2]'}
    attribute_map = {'extends_params': 'extends_params', 'common_params': 'common_params'}

    def __init__(self, extends_params=None, common_params=None):
        """ListExtendsParamsResponse

        The model defined in huaweicloud sdk

        :param extends_params: 附加参数列表
        :type extends_params: list[:class:`huaweicloudsdkosm.v2.ExtendsParamV2`]
        :param common_params: 公共附加参数列表
        :type common_params: list[:class:`huaweicloudsdkosm.v2.CommonParamV2`]
        """
        super(ListExtendsParamsResponse, self).__init__()
        self._extends_params = None
        self._common_params = None
        self.discriminator = None
        if extends_params is not None:
            self.extends_params = extends_params
        if common_params is not None:
            self.common_params = common_params

    @property
    def extends_params(self):
        """Gets the extends_params of this ListExtendsParamsResponse.

        附加参数列表

        :return: The extends_params of this ListExtendsParamsResponse.
        :rtype: list[:class:`huaweicloudsdkosm.v2.ExtendsParamV2`]
        """
        return self._extends_params

    @extends_params.setter
    def extends_params(self, extends_params):
        """Sets the extends_params of this ListExtendsParamsResponse.

        附加参数列表

        :param extends_params: The extends_params of this ListExtendsParamsResponse.
        :type extends_params: list[:class:`huaweicloudsdkosm.v2.ExtendsParamV2`]
        """
        self._extends_params = extends_params

    @property
    def common_params(self):
        """Gets the common_params of this ListExtendsParamsResponse.

        公共附加参数列表

        :return: The common_params of this ListExtendsParamsResponse.
        :rtype: list[:class:`huaweicloudsdkosm.v2.CommonParamV2`]
        """
        return self._common_params

    @common_params.setter
    def common_params(self, common_params):
        """Sets the common_params of this ListExtendsParamsResponse.

        公共附加参数列表

        :param common_params: The common_params of this ListExtendsParamsResponse.
        :type common_params: list[:class:`huaweicloudsdkosm.v2.CommonParamV2`]
        """
        self._common_params = common_params

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
        if not isinstance(other, ListExtendsParamsResponse):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other