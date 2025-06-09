"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
import User_pb2 as User__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16UserOnlineStatus.proto\x12\x1bAcFunDanmu.Im.Cloud.Profile\x1a\nUser.proto"\xca\x01\n\x10UserOnlineStatus\x12\'\n\x04user\x18\x01 \x01(\x0b2\x19.AcFunDanmu.Im.Basic.User\x12\x17\n\x0flastOfflineTime\x18\x02 \x01(\x03\x12D\n\x06status\x18\x03 \x01(\x0e24.AcFunDanmu.Im.Cloud.Profile.UserOnlineStatus.Status".\n\x06Status\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06ONLINE\x10\x01\x12\x0b\n\x07OFFLINE\x10\x02b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'UserOnlineStatus_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _USERONLINESTATUS._serialized_start = 68
    _USERONLINESTATUS._serialized_end = 270
    _USERONLINESTATUS_STATUS._serialized_start = 224
    _USERONLINESTATUS_STATUS._serialized_end = 270