from msrest.serialization import Model

class MeterCreate(Model):
    """MeterCreate.

    All required parameters must be populated in order to send to Azure.

    :param meter_code: Required. The meter code <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type meter_code: str
    :param meter_info: Required. The meter info <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 50 characters</span>
    :type meter_info: str
    :param commodity_id: Required. The identifier for the meter's commodity
     <span class='property-internal'>Required</span>
    :type commodity_id: int
    :param place_id: Required. The identifier for the place the meter is
     assigned to <span class='property-internal'>Topmost (Place)</span> <span
     class='property-internal'>Required</span>
    :type place_id: int
    :param address: Required.
    :type address: ~energycap.sdk.models.RequiredAddressChild
    :param bill_entry_note: The bill entry note <span
     class='property-internal'>Must be between 0 and 64 characters</span>
    :type bill_entry_note: str
    :param include_in_energy_star: DEPRECATED
     To be included in ENERGY STAR a meter needs to be linked to a meter in
     Portfolio Manager
     This can be done with the PUT place/{placeId}/energyStar/link or the
     ENERGY STAR: Mappings Setup Sheet
    :type include_in_energy_star: bool
    :param properties: An array of meter properties
    :type properties: dict[str, str]
    :param primary_use_id: The identifier for the meter's primary use
    :type primary_use_id: int
    :param meter_type_id: Required. The identifier for the meter type. Allowed
     values include: 1 (standard meter) and 6 (chargeback meter) <span
     class='property-internal'>Required</span>
    :type meter_type_id: int
    :param meter_time_zone_id: The identifier for the meter's time zone. If
     one is not specified, the global default meter time zone will be used.
    :type meter_time_zone_id: int
    :param use_unit_id: The use unit ID is the reporting unit for use for this
     meter.
     It is used to determine initial bill format for this meter.
     If not provided defaults to the common unit for the meter commodity
    :type use_unit_id: int
    :param demand_unit_id: The demand unit ID is the reporting unit for demand
     for this meter.
     It is used to determine initial bill format for this meter.
    :type demand_unit_id: int
    :param meter_description: A description of the meter <span
     class='property-internal'>Must be between 0 and 4000 characters</span>
    :type meter_description: str
    """
    _validation = {'meter_code': {'required': True, 'max_length': 32, 'min_length': 0}, 'meter_info': {'required': True, 'max_length': 50, 'min_length': 0}, 'commodity_id': {'required': True}, 'place_id': {'required': True}, 'address': {'required': True}, 'bill_entry_note': {'max_length': 64, 'min_length': 0}, 'meter_type_id': {'required': True}, 'meter_description': {'max_length': 4000, 'min_length': 0}}
    _attribute_map = {'meter_code': {'key': 'meterCode', 'type': 'str'}, 'meter_info': {'key': 'meterInfo', 'type': 'str'}, 'commodity_id': {'key': 'commodityId', 'type': 'int'}, 'place_id': {'key': 'placeId', 'type': 'int'}, 'address': {'key': 'address', 'type': 'RequiredAddressChild'}, 'bill_entry_note': {'key': 'billEntryNote', 'type': 'str'}, 'include_in_energy_star': {'key': 'includeInEnergyStar', 'type': 'bool'}, 'properties': {'key': 'properties', 'type': '{str}'}, 'primary_use_id': {'key': 'primaryUseId', 'type': 'int'}, 'meter_type_id': {'key': 'meterTypeId', 'type': 'int'}, 'meter_time_zone_id': {'key': 'meterTimeZoneId', 'type': 'int'}, 'use_unit_id': {'key': 'useUnitId', 'type': 'int'}, 'demand_unit_id': {'key': 'demandUnitId', 'type': 'int'}, 'meter_description': {'key': 'meterDescription', 'type': 'str'}}

    def __init__(self, *, meter_code: str, meter_info: str, commodity_id: int, place_id: int, address, meter_type_id: int, bill_entry_note: str=None, include_in_energy_star: bool=None, properties=None, primary_use_id: int=None, meter_time_zone_id: int=None, use_unit_id: int=None, demand_unit_id: int=None, meter_description: str=None, **kwargs) -> None:
        super(MeterCreate, self).__init__(**kwargs)
        self.meter_code = meter_code
        self.meter_info = meter_info
        self.commodity_id = commodity_id
        self.place_id = place_id
        self.address = address
        self.bill_entry_note = bill_entry_note
        self.include_in_energy_star = include_in_energy_star
        self.properties = properties
        self.primary_use_id = primary_use_id
        self.meter_type_id = meter_type_id
        self.meter_time_zone_id = meter_time_zone_id
        self.use_unit_id = use_unit_id
        self.demand_unit_id = demand_unit_id
        self.meter_description = meter_description