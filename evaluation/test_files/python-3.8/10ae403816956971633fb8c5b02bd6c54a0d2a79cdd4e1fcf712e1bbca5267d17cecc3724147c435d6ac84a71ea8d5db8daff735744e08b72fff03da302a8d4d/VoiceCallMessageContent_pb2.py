"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
import CallStatus_pb2 as CallStatus__pb2
import CallType_pb2 as CallType__pb2
import ChatMode_pb2 as ChatMode__pb2
import User_pb2 as User__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dVoiceCallMessageContent.proto\x12\x1bAcFunDanmu.Im.Cloud.Message\x1a\x10CallStatus.proto\x1a\x0eCallType.proto\x1a\x0eChatMode.proto\x1a\nUser.proto"\xac\x03\n\x17VoiceCallMessageContent\x12\x0e\n\x06roomId\x18\x01 \x01(\t\x12:\n\x08callType\x18\x02 \x01(\x0e2(.AcFunDanmu.Im.Cloud.Voice.Call.CallType\x12:\n\x06status\x18\x03 \x01(\x0e2*.AcFunDanmu.Im.Cloud.Voice.Call.CallStatus\x12\x13\n\x0bstartTimeMs\x18\x04 \x01(\x03\x12\x11\n\tendTimeMs\x18\x05 \x01(\x03\x12+\n\x08fromUser\x18\x06 \x01(\x0b2\x19.AcFunDanmu.Im.Basic.User\x12:\n\x08chatMode\x18\x07 \x01(\x0e2(.AcFunDanmu.Im.Cloud.Voice.Call.ChatMode\x12\r\n\x05title\x18\x15 \x01(\t\x12\'\n\x04host\x18\x16 \x01(\x0b2\x19.AcFunDanmu.Im.Basic.User\x12.\n\x0bparticipant\x18\x17 \x03(\x0b2\x19.AcFunDanmu.Im.Basic.User\x12\x10\n\x08maxCount\x18\x18 \x01(\x05b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'VoiceCallMessageContent_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _VOICECALLMESSAGECONTENT._serialized_start = 125
    _VOICECALLMESSAGECONTENT._serialized_end = 553