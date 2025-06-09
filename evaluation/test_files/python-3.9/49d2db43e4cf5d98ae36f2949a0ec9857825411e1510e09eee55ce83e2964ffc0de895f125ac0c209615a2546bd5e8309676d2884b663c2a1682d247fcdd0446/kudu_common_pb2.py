"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
import clickzetta.proto.generated.row_operations_pb2 as row__operations__pb2
import clickzetta.proto.generated.block_bloom_filter_pb2 as block__bloom__filter__pb2
import clickzetta.proto.generated.compression_pb2 as compression__pb2
import clickzetta.proto.generated.hash_pb2 as hash__pb2
import clickzetta.proto.generated.pb_util_pb2 as pb__util__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11kudu_common.proto\x12\x04kudu\x1a\x14row_operations.proto\x1a\x18block_bloom_filter.proto\x1a\x11compression.proto\x1a\nhash.proto\x1a\rpb_util.proto"b\n\x16ColumnTypeAttributesPB\x12\x11\n\tprecision\x18\x01 \x01(\x05\x12\r\n\x05scale\x18\x02 \x01(\x05\x12\x0e\n\x06length\x18\x03 \x01(\x05\x12\x16\n\x0especialColCode\x18\x04 \x01(\x05"\x8f\x03\n\x0eColumnSchemaPB\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x02(\t\x12\x1c\n\x04type\x18\x03 \x02(\x0e2\x0e.kudu.DataType\x12\x15\n\x06is_key\x18\x04 \x01(\x08:\x05false\x12\x1a\n\x0bis_nullable\x18\x05 \x01(\x08:\x05false\x12\x1a\n\x12read_default_value\x18\x06 \x01(\x0c\x12\x1b\n\x13write_default_value\x18\x07 \x01(\x0c\x123\n\x08encoding\x18\x08 \x01(\x0e2\x12.kudu.EncodingType:\rAUTO_ENCODING\x12?\n\x0bcompression\x18\t \x01(\x0e2\x15.kudu.CompressionType:\x13DEFAULT_COMPRESSION\x12\x1b\n\x10cfile_block_size\x18\n \x01(\x05:\x010\x125\n\x0ftype_attributes\x18\x0b \x01(\x0b2\x1c.kudu.ColumnTypeAttributesPB\x12\x0f\n\x07comment\x18\x0c \x01(\t"\xdf\x01\n\x13ColumnSchemaDeltaPB\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08new_name\x18\x02 \x01(\t\x12\x15\n\rdefault_value\x18\x04 \x01(\x0c\x12\x16\n\x0eremove_default\x18\x05 \x01(\x08\x12$\n\x08encoding\x18\x06 \x01(\x0e2\x12.kudu.EncodingType\x12*\n\x0bcompression\x18\x07 \x01(\x0e2\x15.kudu.CompressionType\x12\x12\n\nblock_size\x18\x08 \x01(\x05\x12\x13\n\x0bnew_comment\x18\t \x01(\t"1\n\x08SchemaPB\x12%\n\x07columns\x18\x01 \x03(\x0b2\x14.kudu.ColumnSchemaPB"(\n\nHostPortPB\x12\x0c\n\x04host\x18\x01 \x02(\t\x12\x0c\n\x04port\x18\x02 \x02(\r"\xab\x05\n\x11PartitionSchemaPB\x12?\n\x0bhash_schema\x18\x01 \x03(\x0b2*.kudu.PartitionSchemaPB.HashBucketSchemaPB\x12;\n\x0crange_schema\x18\x02 \x01(\x0b2%.kudu.PartitionSchemaPB.RangeSchemaPB\x12P\n\x19custom_hash_schema_ranges\x18\x05 \x03(\x0b2-.kudu.PartitionSchemaPB.RangeWithHashSchemaPB\x1a@\n\x12ColumnIdentifierPB\x12\x0c\n\x02id\x18\x01 \x01(\x05H\x00\x12\x0e\n\x04name\x18\x02 \x01(\tH\x00B\x0c\n\nidentifier\x1aL\n\rRangeSchemaPB\x12;\n\x07columns\x18\x01 \x03(\x0b2*.kudu.PartitionSchemaPB.ColumnIdentifierPB\x1a\xa1\x01\n\x12HashBucketSchemaPB\x12;\n\x07columns\x18\x01 \x03(\x0b2*.kudu.PartitionSchemaPB.ColumnIdentifierPB\x12\x13\n\x0bnum_buckets\x18\x02 \x02(\x05\x12\x0c\n\x04seed\x18\x03 \x01(\r\x12+\n\x0ehash_algorithm\x18\x04 \x01(\x0e2\x13.kudu.HashAlgorithm\x1a\x85\x01\n\x15RangeWithHashSchemaPB\x12+\n\x0crange_bounds\x18\x01 \x01(\x0b2\x15.kudu.RowOperationsPB\x12?\n\x0bhash_schema\x18\x02 \x03(\x0b2*.kudu.PartitionSchemaPB.HashBucketSchemaPBJ\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05"_\n\x0bPartitionPB\x12\x18\n\x0chash_buckets\x18\x01 \x03(\x05B\x02\x10\x01\x12\x1b\n\x13partition_key_start\x18\x02 \x01(\x0c\x12\x19\n\x11partition_key_end\x18\x03 \x01(\x0c"\xef\x04\n\x11ColumnPredicatePB\x12\x0e\n\x06column\x18\x01 \x01(\t\x12.\n\x05range\x18\x02 \x01(\x0b2\x1d.kudu.ColumnPredicatePB.RangeH\x00\x124\n\x08equality\x18\x03 \x01(\x0b2 .kudu.ColumnPredicatePB.EqualityH\x00\x128\n\x0bis_not_null\x18\x04 \x01(\x0b2!.kudu.ColumnPredicatePB.IsNotNullH\x00\x121\n\x07in_list\x18\x05 \x01(\x0b2\x1e.kudu.ColumnPredicatePB.InListH\x00\x121\n\x07is_null\x18\x06 \x01(\x0b2\x1e.kudu.ColumnPredicatePB.IsNullH\x00\x12@\n\x0fin_bloom_filter\x18\x07 \x01(\x0b2%.kudu.ColumnPredicatePB.InBloomFilterH\x00\x1a1\n\x05Range\x12\x13\n\x05lower\x18\x01 \x01(\x0cB\x04\x88\xb5\x18\x01\x12\x13\n\x05upper\x18\x02 \x01(\x0cB\x04\x88\xb5\x18\x01\x1a\x1f\n\x08Equality\x12\x13\n\x05value\x18\x01 \x01(\x0cB\x04\x88\xb5\x18\x01\x1a\x1e\n\x06InList\x12\x14\n\x06values\x18\x01 \x03(\x0cB\x04\x88\xb5\x18\x01\x1a\x0b\n\tIsNotNull\x1a\x08\n\x06IsNull\x1aj\n\rInBloomFilter\x12/\n\rbloom_filters\x18\x01 \x03(\x0b2\x18.kudu.BlockBloomFilterPB\x12\x13\n\x05lower\x18\x02 \x01(\x0cB\x04\x88\xb5\x18\x01\x12\x13\n\x05upper\x18\x03 \x01(\x0cB\x04\x88\xb5\x18\x01B\x0b\n\tpredicate"k\n\nKeyRangePB\x12\x1f\n\x11start_primary_key\x18\x01 \x01(\x0cB\x04\x88\xb5\x18\x01\x12\x1e\n\x10stop_primary_key\x18\x02 \x01(\x0cB\x04\x88\xb5\x18\x01\x12\x1c\n\x14size_bytes_estimates\x18\x03 \x02(\x04"k\n\x12TableExtraConfigPB\x12\x1b\n\x13history_max_age_sec\x18\x01 \x01(\x05\x12\x1c\n\x14maintenance_priority\x18\x02 \x01(\x05\x12\x1a\n\x12disable_compaction\x18\x03 \x01(\x08*\xa6\x02\n\x08DataType\x12\x11\n\x0cUNKNOWN_DATA\x10\xe7\x07\x12\t\n\x05UINT8\x10\x00\x12\x08\n\x04INT8\x10\x01\x12\n\n\x06UINT16\x10\x02\x12\t\n\x05INT16\x10\x03\x12\n\n\x06UINT32\x10\x04\x12\t\n\x05INT32\x10\x05\x12\n\n\x06UINT64\x10\x06\x12\t\n\x05INT64\x10\x07\x12\n\n\x06STRING\x10\x08\x12\x08\n\x04BOOL\x10\t\x12\t\n\x05FLOAT\x10\n\x12\n\n\x06DOUBLE\x10\x0b\x12\n\n\x06BINARY\x10\x0c\x12\x13\n\x0fUNIXTIME_MICROS\x10\r\x12\n\n\x06INT128\x10\x0e\x12\r\n\tDECIMAL32\x10\x0f\x12\r\n\tDECIMAL64\x10\x10\x12\x0e\n\nDECIMAL128\x10\x11\x12\x0e\n\nIS_DELETED\x10\x12\x12\x0b\n\x07VARCHAR\x10\x13\x12\x08\n\x04DATE\x10\x14*\xa0\x01\n\x0cEncodingType\x12\x15\n\x10UNKNOWN_ENCODING\x10\xe7\x07\x12\x11\n\rAUTO_ENCODING\x10\x00\x12\x12\n\x0ePLAIN_ENCODING\x10\x01\x12\x13\n\x0fPREFIX_ENCODING\x10\x02\x12\x10\n\x0cGROUP_VARINT\x10\x03\x12\x07\n\x03RLE\x10\x04\x12\x11\n\rDICT_ENCODING\x10\x05\x12\x0f\n\x0bBIT_SHUFFLE\x10\x06*l\n\x07HmsMode\x12\x08\n\x04NONE\x10\x00\x12\x1a\n\x16DISABLE_HIVE_METASTORE\x10\x03\x12\x19\n\x15ENABLE_HIVE_METASTORE\x10\x01\x12 \n\x1cENABLE_METASTORE_INTEGRATION\x10\x02*h\n\x17ExternalConsistencyMode\x12%\n!UNKNOWN_EXTERNAL_CONSISTENCY_MODE\x10\x00\x12\x15\n\x11CLIENT_PROPAGATED\x10\x01\x12\x0f\n\x0bCOMMIT_WAIT\x10\x02*^\n\x08ReadMode\x12\x15\n\x11UNKNOWN_READ_MODE\x10\x00\x12\x0f\n\x0bREAD_LATEST\x10\x01\x12\x14\n\x10READ_AT_SNAPSHOT\x10\x02\x12\x14\n\x10READ_YOUR_WRITES\x10\x03*?\n\tOrderMode\x12\x16\n\x12UNKNOWN_ORDER_MODE\x10\x00\x12\r\n\tUNORDERED\x10\x01\x12\x0b\n\x07ORDERED\x10\x02*W\n\x10ReplicaSelection\x12\x1d\n\x19UNKNOWN_REPLICA_SELECTION\x10\x00\x12\x0f\n\x0bLEADER_ONLY\x10\x01\x12\x13\n\x0fCLOSEST_REPLICA\x10\x02*6\n\x0bTableTypePB\x12\x11\n\rDEFAULT_TABLE\x10\x00\x12\x14\n\x10TXN_STATUS_TABLE\x10\x01B\x11\n\x0forg.apache.kudu')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'kudu_common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x0forg.apache.kudu'
    _PARTITIONPB.fields_by_name['hash_buckets']._options = None
    _PARTITIONPB.fields_by_name['hash_buckets']._serialized_options = b'\x10\x01'
    _COLUMNPREDICATEPB_RANGE.fields_by_name['lower']._options = None
    _COLUMNPREDICATEPB_RANGE.fields_by_name['lower']._serialized_options = b'\x88\xb5\x18\x01'
    _COLUMNPREDICATEPB_RANGE.fields_by_name['upper']._options = None
    _COLUMNPREDICATEPB_RANGE.fields_by_name['upper']._serialized_options = b'\x88\xb5\x18\x01'
    _COLUMNPREDICATEPB_EQUALITY.fields_by_name['value']._options = None
    _COLUMNPREDICATEPB_EQUALITY.fields_by_name['value']._serialized_options = b'\x88\xb5\x18\x01'
    _COLUMNPREDICATEPB_INLIST.fields_by_name['values']._options = None
    _COLUMNPREDICATEPB_INLIST.fields_by_name['values']._serialized_options = b'\x88\xb5\x18\x01'
    _COLUMNPREDICATEPB_INBLOOMFILTER.fields_by_name['lower']._options = None
    _COLUMNPREDICATEPB_INBLOOMFILTER.fields_by_name['lower']._serialized_options = b'\x88\xb5\x18\x01'
    _COLUMNPREDICATEPB_INBLOOMFILTER.fields_by_name['upper']._options = None
    _COLUMNPREDICATEPB_INBLOOMFILTER.fields_by_name['upper']._serialized_options = b'\x88\xb5\x18\x01'
    _KEYRANGEPB.fields_by_name['start_primary_key']._options = None
    _KEYRANGEPB.fields_by_name['start_primary_key']._serialized_options = b'\x88\xb5\x18\x01'
    _KEYRANGEPB.fields_by_name['stop_primary_key']._options = None
    _KEYRANGEPB.fields_by_name['stop_primary_key']._serialized_options = b'\x88\xb5\x18\x01'
    _DATATYPE._serialized_start = 2570
    _DATATYPE._serialized_end = 2864
    _ENCODINGTYPE._serialized_start = 2867
    _ENCODINGTYPE._serialized_end = 3027
    _HMSMODE._serialized_start = 3029
    _HMSMODE._serialized_end = 3137
    _EXTERNALCONSISTENCYMODE._serialized_start = 3139
    _EXTERNALCONSISTENCYMODE._serialized_end = 3243
    _READMODE._serialized_start = 3245
    _READMODE._serialized_end = 3339
    _ORDERMODE._serialized_start = 3341
    _ORDERMODE._serialized_end = 3404
    _REPLICASELECTION._serialized_start = 3406
    _REPLICASELECTION._serialized_end = 3493
    _TABLETYPEPB._serialized_start = 3495
    _TABLETYPEPB._serialized_end = 3549
    _COLUMNTYPEATTRIBUTESPB._serialized_start = 121
    _COLUMNTYPEATTRIBUTESPB._serialized_end = 219
    _COLUMNSCHEMAPB._serialized_start = 222
    _COLUMNSCHEMAPB._serialized_end = 621
    _COLUMNSCHEMADELTAPB._serialized_start = 624
    _COLUMNSCHEMADELTAPB._serialized_end = 847
    _SCHEMAPB._serialized_start = 849
    _SCHEMAPB._serialized_end = 898
    _HOSTPORTPB._serialized_start = 900
    _HOSTPORTPB._serialized_end = 940
    _PARTITIONSCHEMAPB._serialized_start = 943
    _PARTITIONSCHEMAPB._serialized_end = 1626
    _PARTITIONSCHEMAPB_COLUMNIDENTIFIERPB._serialized_start = 1172
    _PARTITIONSCHEMAPB_COLUMNIDENTIFIERPB._serialized_end = 1236
    _PARTITIONSCHEMAPB_RANGESCHEMAPB._serialized_start = 1238
    _PARTITIONSCHEMAPB_RANGESCHEMAPB._serialized_end = 1314
    _PARTITIONSCHEMAPB_HASHBUCKETSCHEMAPB._serialized_start = 1317
    _PARTITIONSCHEMAPB_HASHBUCKETSCHEMAPB._serialized_end = 1478
    _PARTITIONSCHEMAPB_RANGEWITHHASHSCHEMAPB._serialized_start = 1481
    _PARTITIONSCHEMAPB_RANGEWITHHASHSCHEMAPB._serialized_end = 1614
    _PARTITIONPB._serialized_start = 1628
    _PARTITIONPB._serialized_end = 1723
    _COLUMNPREDICATEPB._serialized_start = 1726
    _COLUMNPREDICATEPB._serialized_end = 2349
    _COLUMNPREDICATEPB_RANGE._serialized_start = 2091
    _COLUMNPREDICATEPB_RANGE._serialized_end = 2140
    _COLUMNPREDICATEPB_EQUALITY._serialized_start = 2142
    _COLUMNPREDICATEPB_EQUALITY._serialized_end = 2173
    _COLUMNPREDICATEPB_INLIST._serialized_start = 2175
    _COLUMNPREDICATEPB_INLIST._serialized_end = 2205
    _COLUMNPREDICATEPB_ISNOTNULL._serialized_start = 2207
    _COLUMNPREDICATEPB_ISNOTNULL._serialized_end = 2218
    _COLUMNPREDICATEPB_ISNULL._serialized_start = 2220
    _COLUMNPREDICATEPB_ISNULL._serialized_end = 2228
    _COLUMNPREDICATEPB_INBLOOMFILTER._serialized_start = 2230
    _COLUMNPREDICATEPB_INBLOOMFILTER._serialized_end = 2336
    _KEYRANGEPB._serialized_start = 2351
    _KEYRANGEPB._serialized_end = 2458
    _TABLEEXTRACONFIGPB._serialized_start = 2460
    _TABLEEXTRACONFIGPB._serialized_end = 2567