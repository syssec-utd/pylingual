import pprint
import six
from enum import Enum

class PaymentProcessor:
    swagger_types = {'company_name': 'dict(str, str)', 'description': 'dict(str, str)', 'feature': 'int', 'headquarters_location': 'dict(str, str)', 'id': 'int', 'logo_path': 'str', 'name': 'dict(str, str)', 'product_name': 'dict(str, str)'}
    attribute_map = {'company_name': 'companyName', 'description': 'description', 'feature': 'feature', 'headquarters_location': 'headquartersLocation', 'id': 'id', 'logo_path': 'logoPath', 'name': 'name', 'product_name': 'productName'}
    _company_name = None
    _description = None
    _feature = None
    _headquarters_location = None
    _id = None
    _logo_path = None
    _name = None
    _product_name = None

    def __init__(self, **kwargs):
        self.discriminator = None
        self.company_name = kwargs.get('company_name', None)
        self.description = kwargs.get('description', None)
        self.feature = kwargs.get('feature', None)
        self.headquarters_location = kwargs.get('headquarters_location', None)
        self.id = kwargs.get('id', None)
        self.logo_path = kwargs.get('logo_path', None)
        self.name = kwargs.get('name', None)
        self.product_name = kwargs.get('product_name', None)

    @property
    def company_name(self):
        """Gets the company_name of this PaymentProcessor.

            

        :return: The company_name of this PaymentProcessor.
        :rtype: dict(str, str)
        """
        return self._company_name

    @company_name.setter
    def company_name(self, company_name):
        """Sets the company_name of this PaymentProcessor.

            

        :param company_name: The company_name of this PaymentProcessor.
        :type: dict(str, str)
        """
        self._company_name = company_name

    @property
    def description(self):
        """Gets the description of this PaymentProcessor.

            The description of the object translated into different languages.

        :return: The description of this PaymentProcessor.
        :rtype: dict(str, str)
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PaymentProcessor.

            The description of the object translated into different languages.

        :param description: The description of this PaymentProcessor.
        :type: dict(str, str)
        """
        self._description = description

    @property
    def feature(self):
        """Gets the feature of this PaymentProcessor.

            

        :return: The feature of this PaymentProcessor.
        :rtype: int
        """
        return self._feature

    @feature.setter
    def feature(self, feature):
        """Sets the feature of this PaymentProcessor.

            

        :param feature: The feature of this PaymentProcessor.
        :type: int
        """
        self._feature = feature

    @property
    def headquarters_location(self):
        """Gets the headquarters_location of this PaymentProcessor.

            

        :return: The headquarters_location of this PaymentProcessor.
        :rtype: dict(str, str)
        """
        return self._headquarters_location

    @headquarters_location.setter
    def headquarters_location(self, headquarters_location):
        """Sets the headquarters_location of this PaymentProcessor.

            

        :param headquarters_location: The headquarters_location of this PaymentProcessor.
        :type: dict(str, str)
        """
        self._headquarters_location = headquarters_location

    @property
    def id(self):
        """Gets the id of this PaymentProcessor.

            A unique identifier for the object.

        :return: The id of this PaymentProcessor.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PaymentProcessor.

            A unique identifier for the object.

        :param id: The id of this PaymentProcessor.
        :type: int
        """
        self._id = id

    @property
    def logo_path(self):
        """Gets the logo_path of this PaymentProcessor.

            

        :return: The logo_path of this PaymentProcessor.
        :rtype: str
        """
        return self._logo_path

    @logo_path.setter
    def logo_path(self, logo_path):
        """Sets the logo_path of this PaymentProcessor.

            

        :param logo_path: The logo_path of this PaymentProcessor.
        :type: str
        """
        self._logo_path = logo_path

    @property
    def name(self):
        """Gets the name of this PaymentProcessor.

            The name of the object translated into different languages.

        :return: The name of this PaymentProcessor.
        :rtype: dict(str, str)
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PaymentProcessor.

            The name of the object translated into different languages.

        :param name: The name of this PaymentProcessor.
        :type: dict(str, str)
        """
        self._name = name

    @property
    def product_name(self):
        """Gets the product_name of this PaymentProcessor.

            

        :return: The product_name of this PaymentProcessor.
        :rtype: dict(str, str)
        """
        return self._product_name

    @product_name.setter
    def product_name(self, product_name):
        """Sets the product_name of this PaymentProcessor.

            

        :param product_name: The product_name of this PaymentProcessor.
        :type: dict(str, str)
        """
        self._product_name = product_name

    def to_dict(self):
        result = {}
        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, 'to_dict') else x, value))
            elif hasattr(value, 'to_dict'):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(lambda item: (item[0], item[1].to_dict()) if hasattr(item[1], 'to_dict') else item, value.items()))
            elif isinstance(value, Enum):
                result[attr] = value.value
            else:
                result[attr] = value
        if issubclass(PaymentProcessor, dict):
            for key, value in self.items():
                result[key] = value
        return result

    def to_str(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.to_str()

    def __eq__(self, other):
        if not isinstance(other, PaymentProcessor):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other