"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ydb.core.yq.libs.config.protos import storage_pb2 as ydb_dot_core_dot_yq_dot_libs_dot_config_dot_protos_dot_storage__pb2
from ydb.library.yql.dq.actors.protos import dq_status_codes_pb2 as ydb_dot_library_dot_yql_dot_dq_dot_actors_dot_protos_dot_dq__status__codes__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n:ydb/core/yq/libs/config/protos/control_plane_storage.proto\x12\x0bNYq.NConfig\x1a,ydb/core/yq/libs/config/protos/storage.proto\x1a6ydb/library/yql/dq/actors/protos/dq_status_codes.proto"&\n\x08TMapItem\x12\x0b\n\x03Key\x18\x01 \x01(\t\x12\r\n\x05Value\x18\x02 \x01(\t"\x8f\x01\n\rTQueryMapping\x122\n\x13CloudIdToTenantName\x18\x01 \x03(\x0b2\x15.NYq.NConfig.TMapItem\x120\n\x11ScopeToTenantName\x18\x02 \x03(\x0b2\x15.NYq.NConfig.TMapItem\x12\x18\n\x10CommonTenantName\x18\x03 \x03(\t"N\n\x0cTRetryPolicy\x12\x12\n\nRetryCount\x18\x01 \x01(\x04\x12\x13\n\x0bRetryPeriod\x18\x02 \x01(\t\x12\x15\n\rBackoffPeriod\x18\x03 \x01(\t"y\n\x13TRetryPolicyMapping\x127\n\nStatusCode\x18\x01 \x03(\x0e2#.NYql.NDqProto.StatusIds.StatusCode\x12)\n\x06Policy\x18\x02 \x01(\x0b2\x19.NYq.NConfig.TRetryPolicy"\xb7\x07\n\x1aTControlPlaneStorageConfig\x12\x0f\n\x07Enabled\x18\x01 \x01(\x08\x12/\n\x07Storage\x18\x02 \x01(\x0b2\x1e.NYq.NConfig.TYdbStorageConfig\x12\x1a\n\x12IdempotencyKeysTtl\x18\x03 \x01(\t\x12\x16\n\x0eMaxRequestSize\x18\x04 \x01(\x04\x12\x17\n\x0fMaxCountQueries\x18\x05 \x01(\x04\x12\x1b\n\x13MaxCountConnections\x18\x06 \x01(\x04\x12\x18\n\x10MaxCountBindings\x18\x07 \x01(\x04\x12\x14\n\x0cMaxCountJobs\x18\x08 \x01(\x04\x12\x12\n\nSuperUsers\x18\t \x03(\t\x12\x17\n\x0fEnableDebugMode\x18\n \x01(\x08\x12\x19\n\x11EnablePermissions\x18\x0b \x01(\x08\x12\x19\n\x11DisableCurrentIam\x18\x0c \x01(\x08\x12\x13\n\x0bUseInMemory\x18\r \x01(\x08\x12\x16\n\x0eTasksBatchSize\x18\x0e \x01(\x04\x12\x1a\n\x12NumTasksProportion\x18\x0f \x01(\x04\x12"\n\x1aAnalyticsRetryCounterLimit\x18\x10 \x01(\x04\x12"\n\x1aStreamingRetryCounterLimit\x18\x11 \x01(\x04\x12\'\n\x1fAnalyticsRetryCounterUpdateTime\x18\x12 \x01(\t\x12\'\n\x1fStreamingRetryCounterUpdateTime\x18\x13 \x01(\t\x12\x1b\n\x13AutomaticQueriesTtl\x18\x14 \x01(\t\x12\x14\n\x0cTaskLeaseTtl\x18\x15 \x01(\t\x127\n\x14TaskLeaseRetryPolicy\x18\x1b \x01(\x0b2\x19.NYq.NConfig.TRetryPolicy\x12\x1b\n\x13AvailableConnection\x18\x16 \x03(\t\x12\x18\n\x10AvailableBinding\x18\x17 \x03(\t\x12\x15\n\rResultSetsTtl\x18\x18 \x01(\t\x12+\n\x07Mapping\x18\x19 \x01(\x0b2\x1a.NYq.NConfig.TQueryMapping\x12<\n\x12RetryPolicyMapping\x18\x1a \x03(\x0b2 .NYq.NConfig.TRetryPolicyMapping\x12\x10\n\x08QuotaTtl\x18\x1c \x01(\t\x12\x12\n\nMetricsTtl\x18\x1d \x01(\t\x12\x14\n\x0cUseDbMapping\x18\x1e \x01(\x08\x12\x16\n\x0eDbReloadPeriod\x18\x1f \x01(\tB\x1b\n\x16ru.yandex.kikimr.proto\xf8\x01\x01b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ydb.core.yq.libs.config.protos.control_plane_storage_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16ru.yandex.kikimr.proto\xf8\x01\x01'
    _TMAPITEM._serialized_start = 177
    _TMAPITEM._serialized_end = 215
    _TQUERYMAPPING._serialized_start = 218
    _TQUERYMAPPING._serialized_end = 361
    _TRETRYPOLICY._serialized_start = 363
    _TRETRYPOLICY._serialized_end = 441
    _TRETRYPOLICYMAPPING._serialized_start = 443
    _TRETRYPOLICYMAPPING._serialized_end = 564
    _TCONTROLPLANESTORAGECONFIG._serialized_start = 567
    _TCONTROLPLANESTORAGECONFIG._serialized_end = 1518