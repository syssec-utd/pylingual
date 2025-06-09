"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from streamlit.proto import WidgetStates_pb2 as streamlit_dot_proto_dot_WidgetStates__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!streamlit/proto/ClientState.proto\x1a"streamlit/proto/WidgetStates.proto"v\n\x0bClientState\x12\x14\n\x0cquery_string\x18\x01 \x01(\t\x12$\n\rwidget_states\x18\x02 \x01(\x0b2\r.WidgetStates\x12\x18\n\x10page_script_hash\x18\x03 \x01(\t\x12\x11\n\tpage_name\x18\x04 \x01(\tb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'streamlit.proto.ClientState_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _CLIENTSTATE._serialized_start = 73
    _CLIENTSTATE._serialized_end = 191