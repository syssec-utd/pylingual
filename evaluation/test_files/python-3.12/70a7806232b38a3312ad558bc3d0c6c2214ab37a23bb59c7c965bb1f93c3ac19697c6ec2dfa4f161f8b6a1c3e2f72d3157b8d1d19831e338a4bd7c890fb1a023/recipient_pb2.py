"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='waves/recipient.proto', package='waves', syntax='proto3', serialized_options=b'\n&com.wavesplatform.protobuf.transactionZ9github.com/wavesplatform/gowaves/pkg/grpc/generated/waves\xaa\x02\x05Waves', create_key=_descriptor._internal_create_key, serialized_pb=b'\n\x15waves/recipient.proto\x12\x05waves"D\n\tRecipient\x12\x19\n\x0fpublic_key_hash\x18\x01 \x01(\x0cH\x00\x12\x0f\n\x05alias\x18\x02 \x01(\tH\x00B\x0b\n\trecipientBk\n&com.wavesplatform.protobuf.transactionZ9github.com/wavesplatform/gowaves/pkg/grpc/generated/waves\xaa\x02\x05Wavesb\x06proto3')
_RECIPIENT = _descriptor.Descriptor(name='Recipient', full_name='waves.Recipient', filename=None, file=DESCRIPTOR, containing_type=None, create_key=_descriptor._internal_create_key, fields=[_descriptor.FieldDescriptor(name='public_key_hash', full_name='waves.Recipient.public_key_hash', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=b'', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key), _descriptor.FieldDescriptor(name='alias', full_name='waves.Recipient.alias', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=b''.decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[_descriptor.OneofDescriptor(name='recipient', full_name='waves.Recipient.recipient', index=0, containing_type=None, create_key=_descriptor._internal_create_key, fields=[])], serialized_start=32, serialized_end=100)
_RECIPIENT.oneofs_by_name['recipient'].fields.append(_RECIPIENT.fields_by_name['public_key_hash'])
_RECIPIENT.fields_by_name['public_key_hash'].containing_oneof = _RECIPIENT.oneofs_by_name['recipient']
_RECIPIENT.oneofs_by_name['recipient'].fields.append(_RECIPIENT.fields_by_name['alias'])
_RECIPIENT.fields_by_name['alias'].containing_oneof = _RECIPIENT.oneofs_by_name['recipient']
DESCRIPTOR.message_types_by_name['Recipient'] = _RECIPIENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
Recipient = _reflection.GeneratedProtocolMessageType('Recipient', (_message.Message,), {'DESCRIPTOR': _RECIPIENT, '__module__': 'waves.recipient_pb2'})
_sym_db.RegisterMessage(Recipient)
DESCRIPTOR._options = None