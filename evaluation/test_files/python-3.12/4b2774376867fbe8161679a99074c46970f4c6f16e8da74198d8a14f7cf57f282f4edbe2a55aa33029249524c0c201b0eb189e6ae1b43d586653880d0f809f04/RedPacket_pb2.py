"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fRedPacket.proto\x12\x1bAcFunDanmu.Im.Cloud.Message"\xd8\x02\n\tRedPacket\x12\x13\n\x0bredPacketId\x18\x01 \x01(\t\x12K\n\rredPacketType\x18\x02 \x01(\x0e24.AcFunDanmu.Im.Cloud.Message.RedPacket.RedPacketType\x12\r\n\x05extra\x18\x03 \x01(\x0c\x12\x13\n\x0bassignedUid\x18\x04 \x01(\x03"\xc4\x01\n\rRedPacketType\x12\x1b\n\x17UNKNOWN_RED_PACKET_TYPE\x10\x00\x12\x0c\n\x08PERSONAL\x10\x01\x12\x17\n\x13GROUP_RANDOM_AMOUNT\x10\x02\x12\x1a\n\x16GROUP_IDENTICAL_AMOUNT\x10\x03\x12\'\n#GROUP_ASSIGNED_MEMBER_RANDOM_AMOUNT\x10\x04\x12*\n&GROUP_ASSIGNED_MEMBER_IDENTICAL_AMOUNT\x10\x05b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'RedPacket_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _REDPACKET._serialized_start = 49
    _REDPACKET._serialized_end = 393
    _REDPACKET_REDPACKETTYPE._serialized_start = 197
    _REDPACKET_REDPACKETTYPE._serialized_end = 393