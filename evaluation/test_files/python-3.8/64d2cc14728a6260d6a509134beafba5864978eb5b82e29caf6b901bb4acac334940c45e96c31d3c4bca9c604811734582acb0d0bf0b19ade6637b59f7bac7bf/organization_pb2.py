"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from layerapi.api import ids_pb2 as api_dot_ids__pb2
from layerapi.api.value import date_pb2 as api_dot_value_dot_date__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dapi/entity/organization.proto\x12\x03api\x1a\rapi/ids.proto\x1a\x14api/value/date.proto"\x9d\x02\n\x0cOrganization\x12\x1f\n\x02id\x18\x01 \x01(\x0b2\x13.api.OrganizationId\x12*\n\x08auth0_id\x18\x02 \x01(\x0b2\x18.api.Auth0OrganizationId\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x14\n\x0cdisplay_name\x18\x04 \x01(\t\x12\x0f\n\x07enabled\x18\x05 \x01(\x08\x12\x0f\n\x07domains\x18\x06 \x03(\t\x12\x17\n\x0fcredits_balance\x18\x08 \x01(\t\x12\x1f\n\x0ccreated_date\x18\t \x01(\x0b2\t.api.Date\x12\x1c\n\x07tier_id\x18\n \x01(\x0b2\x0b.api.TierId\x12"\n\naccount_id\x18\x0b \x01(\x0b2\x0e.api.AccountIdB\x11\n\rcom.layer.apiP\x01b\x06proto3')
_ORGANIZATION = DESCRIPTOR.message_types_by_name['Organization']
Organization = _reflection.GeneratedProtocolMessageType('Organization', (_message.Message,), {'DESCRIPTOR': _ORGANIZATION, '__module__': 'api.entity.organization_pb2'})
_sym_db.RegisterMessage(Organization)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\rcom.layer.apiP\x01'
    _ORGANIZATION._serialized_start = 76
    _ORGANIZATION._serialized_end = 361