import re
import six
from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization

class ListCertificatesResponse(SdkResponse):
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'items': 'list[CertificateBody]', 'total': 'int'}
    attribute_map = {'items': 'items', 'total': 'total'}

    def __init__(self, items=None, total=None):
        """ListCertificatesResponse

        The model defined in huaweicloud sdk

        :param items: 证书列表
        :type items: list[:class:`huaweicloudsdkwaf.v1.CertificateBody`]
        :param total: 证书总数
        :type total: int
        """
        super(ListCertificatesResponse, self).__init__()
        self._items = None
        self._total = None
        self.discriminator = None
        if items is not None:
            self.items = items
        if total is not None:
            self.total = total

    @property
    def items(self):
        """Gets the items of this ListCertificatesResponse.

        证书列表

        :return: The items of this ListCertificatesResponse.
        :rtype: list[:class:`huaweicloudsdkwaf.v1.CertificateBody`]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this ListCertificatesResponse.

        证书列表

        :param items: The items of this ListCertificatesResponse.
        :type items: list[:class:`huaweicloudsdkwaf.v1.CertificateBody`]
        """
        self._items = items

    @property
    def total(self):
        """Gets the total of this ListCertificatesResponse.

        证书总数

        :return: The total of this ListCertificatesResponse.
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this ListCertificatesResponse.

        证书总数

        :param total: The total of this ListCertificatesResponse.
        :type total: int
        """
        self._total = total

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
        if not isinstance(other, ListCertificatesResponse):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other