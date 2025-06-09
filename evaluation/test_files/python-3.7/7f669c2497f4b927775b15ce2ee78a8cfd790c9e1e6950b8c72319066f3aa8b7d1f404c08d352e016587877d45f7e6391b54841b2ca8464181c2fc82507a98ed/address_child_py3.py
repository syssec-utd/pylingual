from msrest.serialization import Model

class AddressChild(Model):
    """AddressChild.

    :param address_type_id: The address type identifier
    :type address_type_id: int
    :param line1: The line 1 of the address <span
     class='property-internal'>Must be between 0 and 100 characters</span>
    :type line1: str
    :param line2: The line 2 of the address <span
     class='property-internal'>Must be between 0 and 100 characters</span>
    :type line2: str
    :param line3: The line 3 of the address <span
     class='property-internal'>Must be between 0 and 100 characters</span>.
     Default value: "Æ" .
    :type line3: str
    :param city: The city of the place <span class='property-internal'>Must be
     between 0 and 100 characters</span>
    :type city: str
    :param state: The state of the place <span class='property-internal'>Must
     be between 0 and 100 characters</span>
    :type state: str
    :param country: The country of the place <span
     class='property-internal'>Must be between 0 and 64 characters</span>
    :type country: str
    :param postal_code: The postal code of the place <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type postal_code: str
    :param latitude: The latitude of the place
     Required when the country is not United States or Canada <span
     class='property-internal'>Must be between -90 and 90</span>
    :type latitude: float
    :param longitude: The longitude of the place
     Required when the country is not United States or Canada <span
     class='property-internal'>Must be between -180 and 180</span>
    :type longitude: float
    """
    _validation = {'line1': {'max_length': 100, 'min_length': 0}, 'line2': {'max_length': 100, 'min_length': 0}, 'line3': {'max_length': 100, 'min_length': 0}, 'city': {'max_length': 100, 'min_length': 0}, 'state': {'max_length': 100, 'min_length': 0}, 'country': {'max_length': 64, 'min_length': 0}, 'postal_code': {'max_length': 32, 'min_length': 0}, 'latitude': {'maximum': 90, 'minimum': -90}, 'longitude': {'maximum': 180, 'minimum': -180}}
    _attribute_map = {'address_type_id': {'key': 'addressTypeId', 'type': 'int'}, 'line1': {'key': 'line1', 'type': 'str'}, 'line2': {'key': 'line2', 'type': 'str'}, 'line3': {'key': 'line3', 'type': 'str'}, 'city': {'key': 'city', 'type': 'str'}, 'state': {'key': 'state', 'type': 'str'}, 'country': {'key': 'country', 'type': 'str'}, 'postal_code': {'key': 'postalCode', 'type': 'str'}, 'latitude': {'key': 'latitude', 'type': 'float'}, 'longitude': {'key': 'longitude', 'type': 'float'}}

    def __init__(self, *, address_type_id: int=None, line1: str=None, line2: str=None, line3: str='Æ', city: str=None, state: str=None, country: str=None, postal_code: str=None, latitude: float=None, longitude: float=None, **kwargs) -> None:
        super(AddressChild, self).__init__(**kwargs)
        self.address_type_id = address_type_id
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude