import re
import six
from g42cloudsdkcore.utils.http_utils import sanitize_for_serialization

class VaultAssociate:
    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    openapi_types = {'destination_vault_id': 'str', 'policy_id': 'str', 'add_policy_ids': 'list[str]'}
    attribute_map = {'destination_vault_id': 'destination_vault_id', 'policy_id': 'policy_id', 'add_policy_ids': 'add_policy_ids'}

    def __init__(self, destination_vault_id=None, policy_id=None, add_policy_ids=None):
        """VaultAssociate

        The model defined in g42cloud sdk

        :param destination_vault_id: The param of the VaultAssociate
        :type destination_vault_id: str
        :param policy_id: The param of the VaultAssociate
        :type policy_id: str
        :param add_policy_ids: The param of the VaultAssociate
        :type add_policy_ids: list[str]
        """
        self._destination_vault_id = None
        self._policy_id = None
        self._add_policy_ids = None
        self.discriminator = None
        if destination_vault_id is not None:
            self.destination_vault_id = destination_vault_id
        if policy_id is not None:
            self.policy_id = policy_id
        if add_policy_ids is not None:
            self.add_policy_ids = add_policy_ids

    @property
    def destination_vault_id(self):
        """Gets the destination_vault_id of this VaultAssociate.

        :return: The destination_vault_id of this VaultAssociate.
        :rtype: str
        """
        return self._destination_vault_id

    @destination_vault_id.setter
    def destination_vault_id(self, destination_vault_id):
        """Sets the destination_vault_id of this VaultAssociate.

        :param destination_vault_id: The destination_vault_id of this VaultAssociate.
        :type destination_vault_id: str
        """
        self._destination_vault_id = destination_vault_id

    @property
    def policy_id(self):
        """Gets the policy_id of this VaultAssociate.

        :return: The policy_id of this VaultAssociate.
        :rtype: str
        """
        return self._policy_id

    @policy_id.setter
    def policy_id(self, policy_id):
        """Sets the policy_id of this VaultAssociate.

        :param policy_id: The policy_id of this VaultAssociate.
        :type policy_id: str
        """
        self._policy_id = policy_id

    @property
    def add_policy_ids(self):
        """Gets the add_policy_ids of this VaultAssociate.

        :return: The add_policy_ids of this VaultAssociate.
        :rtype: list[str]
        """
        return self._add_policy_ids

    @add_policy_ids.setter
    def add_policy_ids(self, add_policy_ids):
        """Sets the add_policy_ids of this VaultAssociate.

        :param add_policy_ids: The add_policy_ids of this VaultAssociate.
        :type add_policy_ids: list[str]
        """
        self._add_policy_ids = add_policy_ids

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
        if not isinstance(other, VaultAssociate):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other