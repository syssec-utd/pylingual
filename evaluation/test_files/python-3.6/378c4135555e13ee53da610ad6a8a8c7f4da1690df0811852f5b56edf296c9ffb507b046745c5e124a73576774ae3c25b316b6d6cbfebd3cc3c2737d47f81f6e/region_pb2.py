"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&spaceone/api/inventory/v1/region.proto\x12\x19spaceone.api.inventory.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto"\x84\x01\n\x13CreateRegionRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0bregion_code\x18\x02 \x01(\t\x12\x10\n\x08provider\x18\x03 \x01(\t\x12%\n\x04tags\x18\x04 \x01(\x0b2\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x05 \x01(\t"p\n\x13UpdateRegionRequest\x12\x11\n\tregion_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04tags\x18\x03 \x01(\x0b2\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x04 \x01(\t"5\n\rRegionRequest\x12\x11\n\tregion_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t"F\n\x10GetRegionRequest\x12\x11\n\tregion_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t"\xa8\x01\n\x0bRegionQuery\x12*\n\x05query\x18\x01 \x01(\x0b2\x1b.spaceone.api.core.v1.Query\x12\x11\n\tregion_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nregion_key\x18\x04 \x01(\t\x12\x13\n\x0bregion_code\x18\x05 \x01(\t\x12\x10\n\x08provider\x18\x06 \x01(\t\x12\x11\n\tdomain_id\x18\x07 \x01(\t"\xca\x01\n\nRegionInfo\x12\x11\n\tregion_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\nregion_key\x18\x03 \x01(\t\x12\x13\n\x0bregion_code\x18\x04 \x01(\t\x12\x10\n\x08provider\x18\x05 \x01(\t\x12%\n\x04tags\x18\x06 \x01(\x0b2\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x07 \x01(\t\x12\x12\n\ncreated_at\x18\x08 \x01(\t\x12\x12\n\nupdated_at\x18\t \x01(\t"Z\n\x0bRegionsInfo\x126\n\x07results\x18\x01 \x03(\x0b2%.spaceone.api.inventory.v1.RegionInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05"Z\n\x0fRegionStatQuery\x124\n\x05query\x18\x01 \x01(\x0b2%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\x99\x06\n\x06Region\x12~\n\x06create\x12..spaceone.api.inventory.v1.CreateRegionRequest\x1a%.spaceone.api.inventory.v1.RegionInfo"\x1d\x82\xd3\xe4\x93\x02\x17"\x15/inventory/v1/regions\x12\x89\x01\n\x06update\x12..spaceone.api.inventory.v1.UpdateRegionRequest\x1a%.spaceone.api.inventory.v1.RegionInfo"(\x82\xd3\xe4\x93\x02"\x1a /inventory/v1/region/{region_id}\x12t\n\x06delete\x12(.spaceone.api.inventory.v1.RegionRequest\x1a\x16.google.protobuf.Empty"(\x82\xd3\xe4\x93\x02"* /inventory/v1/region/{region_id}\x12\x83\x01\n\x03get\x12+.spaceone.api.inventory.v1.GetRegionRequest\x1a%.spaceone.api.inventory.v1.RegionInfo"(\x82\xd3\xe4\x93\x02"\x12 /inventory/v1/region/{region_id}\x12\x95\x01\n\x04list\x12&.spaceone.api.inventory.v1.RegionQuery\x1a&.spaceone.api.inventory.v1.RegionsInfo"=\x82\xd3\xe4\x93\x027\x12\x15/inventory/v1/regionsZ\x1e"\x1c/inventory/v1/regions/search\x12o\n\x04stat\x12*.spaceone.api.inventory.v1.RegionStatQuery\x1a\x17.google.protobuf.Struct""\x82\xd3\xe4\x93\x02\x1c"\x1a/inventory/v1/regions/statb\x06proto3')
_CREATEREGIONREQUEST = DESCRIPTOR.message_types_by_name['CreateRegionRequest']
_UPDATEREGIONREQUEST = DESCRIPTOR.message_types_by_name['UpdateRegionRequest']
_REGIONREQUEST = DESCRIPTOR.message_types_by_name['RegionRequest']
_GETREGIONREQUEST = DESCRIPTOR.message_types_by_name['GetRegionRequest']
_REGIONQUERY = DESCRIPTOR.message_types_by_name['RegionQuery']
_REGIONINFO = DESCRIPTOR.message_types_by_name['RegionInfo']
_REGIONSINFO = DESCRIPTOR.message_types_by_name['RegionsInfo']
_REGIONSTATQUERY = DESCRIPTOR.message_types_by_name['RegionStatQuery']
CreateRegionRequest = _reflection.GeneratedProtocolMessageType('CreateRegionRequest', (_message.Message,), {'DESCRIPTOR': _CREATEREGIONREQUEST, '__module__': 'spaceone.api.inventory.v1.region_pb2'})
_sym_db.RegisterMessage(CreateRegionRequest)
UpdateRegionRequest = _reflection.GeneratedProtocolMessageType('UpdateRegionRequest', (_message.Message,), {'DESCRIPTOR': _UPDATEREGIONREQUEST, '__module__': 'spaceone.api.inventory.v1.region_pb2'})
_sym_db.RegisterMessage(UpdateRegionRequest)
RegionRequest = _reflection.GeneratedProtocolMessageType('RegionRequest', (_message.Message,), {'DESCRIPTOR': _REGIONREQUEST, '__module__': 'spaceone.api.inventory.v1.region_pb2'})
_sym_db.RegisterMessage(RegionRequest)
GetRegionRequest = _reflection.GeneratedProtocolMessageType('GetRegionRequest', (_message.Message,), {'DESCRIPTOR': _GETREGIONREQUEST, '__module__': 'spaceone.api.inventory.v1.region_pb2'})
_sym_db.RegisterMessage(GetRegionRequest)
RegionQuery = _reflection.GeneratedProtocolMessageType('RegionQuery', (_message.Message,), {'DESCRIPTOR': _REGIONQUERY, '__module__': 'spaceone.api.inventory.v1.region_pb2'})
_sym_db.RegisterMessage(RegionQuery)
RegionInfo = _reflection.GeneratedProtocolMessageType('RegionInfo', (_message.Message,), {'DESCRIPTOR': _REGIONINFO, '__module__': 'spaceone.api.inventory.v1.region_pb2'})
_sym_db.RegisterMessage(RegionInfo)
RegionsInfo = _reflection.GeneratedProtocolMessageType('RegionsInfo', (_message.Message,), {'DESCRIPTOR': _REGIONSINFO, '__module__': 'spaceone.api.inventory.v1.region_pb2'})
_sym_db.RegisterMessage(RegionsInfo)
RegionStatQuery = _reflection.GeneratedProtocolMessageType('RegionStatQuery', (_message.Message,), {'DESCRIPTOR': _REGIONSTATQUERY, '__module__': 'spaceone.api.inventory.v1.region_pb2'})
_sym_db.RegisterMessage(RegionStatQuery)
_REGION = DESCRIPTOR.services_by_name['Region']
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _REGION.methods_by_name['create']._options = None
    _REGION.methods_by_name['create']._serialized_options = b'\x82\xd3\xe4\x93\x02\x17"\x15/inventory/v1/regions'
    _REGION.methods_by_name['update']._options = None
    _REGION.methods_by_name['update']._serialized_options = b'\x82\xd3\xe4\x93\x02"\x1a /inventory/v1/region/{region_id}'
    _REGION.methods_by_name['delete']._options = None
    _REGION.methods_by_name['delete']._serialized_options = b'\x82\xd3\xe4\x93\x02"* /inventory/v1/region/{region_id}'
    _REGION.methods_by_name['get']._options = None
    _REGION.methods_by_name['get']._serialized_options = b'\x82\xd3\xe4\x93\x02"\x12 /inventory/v1/region/{region_id}'
    _REGION.methods_by_name['list']._options = None
    _REGION.methods_by_name['list']._serialized_options = b'\x82\xd3\xe4\x93\x027\x12\x15/inventory/v1/regionsZ\x1e"\x1c/inventory/v1/regions/search'
    _REGION.methods_by_name['stat']._options = None
    _REGION.methods_by_name['stat']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1c"\x1a/inventory/v1/regions/stat'
    _CREATEREGIONREQUEST._serialized_start = 193
    _CREATEREGIONREQUEST._serialized_end = 325
    _UPDATEREGIONREQUEST._serialized_start = 327
    _UPDATEREGIONREQUEST._serialized_end = 439
    _REGIONREQUEST._serialized_start = 441
    _REGIONREQUEST._serialized_end = 494
    _GETREGIONREQUEST._serialized_start = 496
    _GETREGIONREQUEST._serialized_end = 566
    _REGIONQUERY._serialized_start = 569
    _REGIONQUERY._serialized_end = 737
    _REGIONINFO._serialized_start = 740
    _REGIONINFO._serialized_end = 942
    _REGIONSINFO._serialized_start = 944
    _REGIONSINFO._serialized_end = 1034
    _REGIONSTATQUERY._serialized_start = 1036
    _REGIONSTATQUERY._serialized_end = 1126
    _REGION._serialized_start = 1129
    _REGION._serialized_end = 1922