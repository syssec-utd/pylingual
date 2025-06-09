"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nCostorlab/agent/message/proto/v3/capture/filesystem/filesystem.proto\x122ostorlab.agent.message.proto.v3.capture.filesystem"\xb6\x01\n\x07Message\x12H\n\x05event\x18\x01 \x01(\x0e29.ostorlab.agent.message.proto.v3.capture.filesystem.Event\x12\x10\n\x08filename\x18\x02 \x01(\t\x12\x0b\n\x03pid\x18\x03 \x01(\x05\x12\x0b\n\x03uid\x18\x04 \x01(\x05\x12\x0b\n\x03gid\x18\x05 \x01(\x05\x12\x0c\n\x04mode\x18\x06 \x01(\x05\x12\x0c\n\x04ppid\x18\x07 \x01(\x05\x12\x0c\n\x04proc\x18\x08 \x01(\t*\x96\x02\n\x05Event\x12\n\n\x06ACCESS\x10\x01\x12\x08\n\x04OPEN\x10\x02\x12\r\n\tOPEN_EXEC\x10\x03\x12\n\n\x06ATTRIB\x10\x04\x12\n\n\x06CREATE\x10\x05\x12\n\n\x06DELETE\x10\x06\x12\x0f\n\x0bDELETE_SELF\x10\x07\x12\x0e\n\nMOVED_FROM\x10\x08\x12\x0c\n\x08MOVED_TO\x10\t\x12\r\n\tMOVE_SELF\x10\n\x12\x0f\n\x0bCLOSE_WRITE\x10\x0b\x12\x11\n\rCLOSE_NOWRITE\x10\x0c\x12\x0e\n\nQ_OVERFLOW\x10\r\x12\x0f\n\x0bACCESS_PERM\x10\x0e\x12\r\n\tOPEN_PERM\x10\x0f\x12\x12\n\x0eOPEN_EXEC_PERM\x10\x10\x12\t\n\x05CLOSE\x10\x11\x12\x08\n\x04MOVE\x10\x12\x12\t\n\x05ONDIR\x10\x13')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ostorlab.agent.message.proto.v3.capture.filesystem.filesystem_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _EVENT._serialized_start = 309
    _EVENT._serialized_end = 587
    _MESSAGE._serialized_start = 124
    _MESSAGE._serialized_end = 306