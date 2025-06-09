import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='other_proto_msgs.proto', package='', syntax='proto3', serialized_options=None, serialized_pb=_b('\n\x16other_proto_msgs.proto".\n\nGenericMsg\x12\x0f\n\x07type_id\x18\x01 \x01(\x05\x12\x0f\n\x07content\x18\x02 \x01(\x0cb\x06proto3'))
_GENERICMSG = _descriptor.Descriptor(name='GenericMsg', full_name='GenericMsg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='type_id', full_name='GenericMsg.type_id', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR), _descriptor.FieldDescriptor(name='content', full_name='GenericMsg.content', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=26, serialized_end=72)
DESCRIPTOR.message_types_by_name['GenericMsg'] = _GENERICMSG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
GenericMsg = _reflection.GeneratedProtocolMessageType('GenericMsg', (_message.Message,), dict(DESCRIPTOR=_GENERICMSG, __module__='other_proto_msgs_pb2'))
_sym_db.RegisterMessage(GenericMsg)