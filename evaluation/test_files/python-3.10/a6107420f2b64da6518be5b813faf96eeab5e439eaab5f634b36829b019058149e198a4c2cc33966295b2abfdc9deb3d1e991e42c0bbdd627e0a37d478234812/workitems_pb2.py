"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from . import ace_pb2 as ace__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fworkitems.proto\x12\x07openiap\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\tace.proto"\xaa\x03\n\x08Workitem\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07payload\x18\x03 \x01(\t\x12\x10\n\x08priority\x18\x04 \x01(\x05\x12+\n\x07nextrun\x18\x05 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12+\n\x07lastrun\x18\x06 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12$\n\x05files\x18\x07 \x03(\x0b2\x15.openiap.WorkitemFile\x12\r\n\x05state\x18\x08 \x01(\t\x12\x0b\n\x03wiq\x18\t \x01(\t\x12\r\n\x05wiqid\x18\n \x01(\t\x12\x0f\n\x07retries\x18\x0b \x01(\x05\x12\x10\n\x08username\x18\x0c \x01(\t\x12\x15\n\rsuccess_wiqid\x18\r \x01(\t\x12\x14\n\x0cfailed_wiqid\x18\x0e \x01(\t\x12\x13\n\x0bsuccess_wiq\x18\x0f \x01(\t\x12\x12\n\nfailed_wiq\x18\x10 \x01(\t\x12\x14\n\x0cerrormessage\x18\x11 \x01(\t\x12\x13\n\x0berrorsource\x18\x12 \x01(\t\x12\x11\n\terrortype\x18\x13 \x01(\t"O\n\x0cWorkitemFile\x12\x10\n\x08filename\x18\x01 \x01(\t\x12\x0b\n\x03_id\x18\x02 \x01(\t\x12\x12\n\ncompressed\x18\x03 \x01(\x08\x12\x0c\n\x04file\x18\x04 \x01(\x0c"\x8b\x02\n\x13PushWorkitemRequest\x12\x0b\n\x03wiq\x18\x01 \x01(\t\x12\r\n\x05wiqid\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07payload\x18\x04 \x01(\t\x12+\n\x07nextrun\x18\x05 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x15\n\rsuccess_wiqid\x18\x06 \x01(\t\x12\x14\n\x0cfailed_wiqid\x18\x07 \x01(\t\x12\x13\n\x0bsuccess_wiq\x18\x08 \x01(\t\x12\x12\n\nfailed_wiq\x18\t \x01(\t\x12\x10\n\x08priority\x18\n \x01(\x05\x12$\n\x05files\x18\x0b \x03(\x0b2\x15.openiap.WorkitemFile";\n\x14PushWorkitemResponse\x12#\n\x08workitem\x18\x01 \x01(\x0b2\x11.openiap.Workitem"\xe9\x01\n\x14PushWorkitemsRequest\x12\x0b\n\x03wiq\x18\x01 \x01(\t\x12\r\n\x05wiqid\x18\x02 \x01(\t\x12+\n\x07nextrun\x18\x03 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x15\n\rsuccess_wiqid\x18\x04 \x01(\t\x12\x14\n\x0cfailed_wiqid\x18\x05 \x01(\t\x12\x13\n\x0bsuccess_wiq\x18\x06 \x01(\t\x12\x12\n\nfailed_wiq\x18\x07 \x01(\t\x12\x10\n\x08priority\x18\x08 \x01(\x05\x12 \n\x05items\x18\t \x03(\x0b2\x11.openiap.Workitem"=\n\x15PushWorkitemsResponse\x12$\n\tworkitems\x18\x01 \x03(\x0b2\x11.openiap.Workitem"|\n\x15UpdateWorkitemRequest\x12#\n\x08workitem\x18\x01 \x01(\x0b2\x11.openiap.Workitem\x12\x18\n\x10ignoremaxretries\x18\x02 \x01(\x08\x12$\n\x05files\x18\x03 \x03(\x0b2\x15.openiap.WorkitemFile"=\n\x16UpdateWorkitemResponse\x12#\n\x08workitem\x18\x01 \x01(\x0b2\x11.openiap.Workitem"Z\n\x12PopWorkitemRequest\x12\x0b\n\x03wiq\x18\x01 \x01(\t\x12\r\n\x05wiqid\x18\x02 \x01(\t\x12\x14\n\x0cincludefiles\x18\x03 \x01(\x08\x12\x12\n\ncompressed\x18\x04 \x01(\x08":\n\x13PopWorkitemResponse\x12#\n\x08workitem\x18\x01 \x01(\x0b2\x11.openiap.Workitem"$\n\x15DeleteWorkitemRequest\x12\x0b\n\x03_id\x18\x01 \x01(\t"\x18\n\x16DeleteWorkitemResponse"\x80\x04\n\rWorkItemQueue\x12\x12\n\nworkflowid\x18\x01 \x01(\t\x12\x12\n\nrobotqueue\x18\x02 \x01(\t\x12\x11\n\tamqpqueue\x18\x03 \x01(\t\x12\x11\n\tprojectid\x18\x04 \x01(\t\x12\x11\n\tusersrole\x18\x05 \x01(\t\x12\x12\n\nmaxretries\x18\x06 \x01(\x05\x12\x12\n\nretrydelay\x18\x07 \x01(\x05\x12\x14\n\x0cinitialdelay\x18\x08 \x01(\x05\x12\x15\n\rsuccess_wiqid\x18\t \x01(\t\x12\x14\n\x0cfailed_wiqid\x18\n \x01(\t\x12\x13\n\x0bsuccess_wiq\x18\x0b \x01(\t\x12\x12\n\nfailed_wiq\x18\x0c \x01(\t\x12\x0b\n\x03_id\x18\r \x01(\t\x12\x1a\n\x04_acl\x18\x0e \x03(\x0b2\x0c.openiap.Ace\x12\x0c\n\x04name\x18\x0f \x01(\t\x12\x14\n\x0c_createdbyid\x18\x10 \x01(\t\x12\x12\n\n_createdby\x18\x11 \x01(\t\x12,\n\x08_created\x18\x12 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x15\n\r_modifiedbyid\x18\x13 \x01(\t\x12\x13\n\x0b_modifiedby\x18\x14 \x01(\t\x12-\n\t_modified\x18\x15 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x10\n\x08_version\x18\x16 \x01(\x05"\xa3\x02\n\x17AddWorkItemQueueRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\nrobotqueue\x18\x02 \x01(\t\x12\x11\n\tamqpqueue\x18\x03 \x01(\t\x12\x11\n\tprojectid\x18\x04 \x01(\t\x12\x10\n\x08skiprole\x18\x05 \x01(\x08\x12\x12\n\nmaxretries\x18\x06 \x01(\x05\x12\x14\n\x0cinitialdelay\x18\x07 \x01(\x05\x12\x12\n\nretrydelay\x18\x08 \x01(\x05\x12\x15\n\rsuccess_wiqid\x18\t \x01(\t\x12\x14\n\x0cfailed_wiqid\x18\n \x01(\t\x12\x13\n\x0bsuccess_wiq\x18\x0b \x01(\t\x12\x12\n\nfailed_wiq\x18\x0c \x01(\t\x12\x1a\n\x04_acl\x18\r \x03(\x0b2\x0c.openiap.Ace"I\n\x18AddWorkItemQueueResponse\x12-\n\rworkitemqueue\x18\x01 \x01(\x0b2\x16.openiap.WorkItemQueueb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'workitems_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _WORKITEM._serialized_start = 73
    _WORKITEM._serialized_end = 499
    _WORKITEMFILE._serialized_start = 501
    _WORKITEMFILE._serialized_end = 580
    _PUSHWORKITEMREQUEST._serialized_start = 583
    _PUSHWORKITEMREQUEST._serialized_end = 850
    _PUSHWORKITEMRESPONSE._serialized_start = 852
    _PUSHWORKITEMRESPONSE._serialized_end = 911
    _PUSHWORKITEMSREQUEST._serialized_start = 914
    _PUSHWORKITEMSREQUEST._serialized_end = 1147
    _PUSHWORKITEMSRESPONSE._serialized_start = 1149
    _PUSHWORKITEMSRESPONSE._serialized_end = 1210
    _UPDATEWORKITEMREQUEST._serialized_start = 1212
    _UPDATEWORKITEMREQUEST._serialized_end = 1336
    _UPDATEWORKITEMRESPONSE._serialized_start = 1338
    _UPDATEWORKITEMRESPONSE._serialized_end = 1399
    _POPWORKITEMREQUEST._serialized_start = 1401
    _POPWORKITEMREQUEST._serialized_end = 1491
    _POPWORKITEMRESPONSE._serialized_start = 1493
    _POPWORKITEMRESPONSE._serialized_end = 1551
    _DELETEWORKITEMREQUEST._serialized_start = 1553
    _DELETEWORKITEMREQUEST._serialized_end = 1589
    _DELETEWORKITEMRESPONSE._serialized_start = 1591
    _DELETEWORKITEMRESPONSE._serialized_end = 1615
    _WORKITEMQUEUE._serialized_start = 1618
    _WORKITEMQUEUE._serialized_end = 2130
    _ADDWORKITEMQUEUEREQUEST._serialized_start = 2133
    _ADDWORKITEMQUEUEREQUEST._serialized_end = 2424
    _ADDWORKITEMQUEUERESPONSE._serialized_start = 2426
    _ADDWORKITEMQUEUERESPONSE._serialized_end = 2499