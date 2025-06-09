"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from flyteidl.core import execution_pb2 as flyteidl_dot_core_dot_execution__pb2
from flyteidl.core import identifier_pb2 as flyteidl_dot_core_dot_identifier__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bflyteidl/admin/common.proto\x12\x0eflyteidl.admin\x1a\x1dflyteidl/core/execution.proto\x1a\x1eflyteidl/core/identifier.proto"]\n\x15NamedEntityIdentifier\x12\x18\n\x07project\x18\x01 \x01(\tR\x07project\x12\x16\n\x06domain\x18\x02 \x01(\tR\x06domain\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name"o\n\x13NamedEntityMetadata\x12 \n\x0bdescription\x18\x01 \x01(\tR\x0bdescription\x126\n\x05state\x18\x02 \x01(\x0e2 .flyteidl.admin.NamedEntityStateR\x05state"\xc7\x01\n\x0bNamedEntity\x12@\n\rresource_type\x18\x01 \x01(\x0e2\x1b.flyteidl.core.ResourceTypeR\x0cresourceType\x125\n\x02id\x18\x02 \x01(\x0b2%.flyteidl.admin.NamedEntityIdentifierR\x02id\x12?\n\x08metadata\x18\x03 \x01(\x0b2#.flyteidl.admin.NamedEntityMetadataR\x08metadata"\x82\x01\n\x04Sort\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12<\n\tdirection\x18\x02 \x01(\x0e2\x1e.flyteidl.admin.Sort.DirectionR\tdirection"*\n\tDirection\x12\x0e\n\nDESCENDING\x10\x00\x12\r\n\tASCENDING\x10\x01"\xc9\x01\n NamedEntityIdentifierListRequest\x12\x18\n\x07project\x18\x01 \x01(\tR\x07project\x12\x16\n\x06domain\x18\x02 \x01(\tR\x06domain\x12\x14\n\x05limit\x18\x03 \x01(\rR\x05limit\x12\x14\n\x05token\x18\x04 \x01(\tR\x05token\x12-\n\x07sort_by\x18\x05 \x01(\x0b2\x14.flyteidl.admin.SortR\x06sortBy\x12\x18\n\x07filters\x18\x06 \x01(\tR\x07filters"\x81\x02\n\x16NamedEntityListRequest\x12@\n\rresource_type\x18\x01 \x01(\x0e2\x1b.flyteidl.core.ResourceTypeR\x0cresourceType\x12\x18\n\x07project\x18\x02 \x01(\tR\x07project\x12\x16\n\x06domain\x18\x03 \x01(\tR\x06domain\x12\x14\n\x05limit\x18\x04 \x01(\rR\x05limit\x12\x14\n\x05token\x18\x05 \x01(\tR\x05token\x12-\n\x07sort_by\x18\x06 \x01(\x0b2\x14.flyteidl.admin.SortR\x06sortBy\x12\x18\n\x07filters\x18\x07 \x01(\tR\x07filters"t\n\x19NamedEntityIdentifierList\x12A\n\x08entities\x18\x01 \x03(\x0b2%.flyteidl.admin.NamedEntityIdentifierR\x08entities\x12\x14\n\x05token\x18\x02 \x01(\tR\x05token"`\n\x0fNamedEntityList\x127\n\x08entities\x18\x01 \x03(\x0b2\x1b.flyteidl.admin.NamedEntityR\x08entities\x12\x14\n\x05token\x18\x02 \x01(\tR\x05token"\x90\x01\n\x15NamedEntityGetRequest\x12@\n\rresource_type\x18\x01 \x01(\x0e2\x1b.flyteidl.core.ResourceTypeR\x0cresourceType\x125\n\x02id\x18\x02 \x01(\x0b2%.flyteidl.admin.NamedEntityIdentifierR\x02id"\xd4\x01\n\x18NamedEntityUpdateRequest\x12@\n\rresource_type\x18\x01 \x01(\x0e2\x1b.flyteidl.core.ResourceTypeR\x0cresourceType\x125\n\x02id\x18\x02 \x01(\x0b2%.flyteidl.admin.NamedEntityIdentifierR\x02id\x12?\n\x08metadata\x18\x03 \x01(\x0b2#.flyteidl.admin.NamedEntityMetadataR\x08metadata"\x1b\n\x19NamedEntityUpdateResponse"=\n\x10ObjectGetRequest\x12)\n\x02id\x18\x01 \x01(\x0b2\x19.flyteidl.core.IdentifierR\x02id"\xc1\x01\n\x13ResourceListRequest\x125\n\x02id\x18\x01 \x01(\x0b2%.flyteidl.admin.NamedEntityIdentifierR\x02id\x12\x14\n\x05limit\x18\x02 \x01(\rR\x05limit\x12\x14\n\x05token\x18\x03 \x01(\tR\x05token\x12\x18\n\x07filters\x18\x04 \x01(\tR\x07filters\x12-\n\x07sort_by\x18\x05 \x01(\x0b2\x14.flyteidl.admin.SortR\x06sortBy">\n\x11EmailNotification\x12)\n\x10recipients_email\x18\x01 \x03(\tR\x0frecipientsEmail"B\n\x15PagerDutyNotification\x12)\n\x10recipients_email\x18\x01 \x03(\tR\x0frecipientsEmail">\n\x11SlackNotification\x12)\n\x10recipients_email\x18\x01 \x03(\tR\x0frecipientsEmail"\x94\x02\n\x0cNotification\x12>\n\x06phases\x18\x01 \x03(\x0e2&.flyteidl.core.WorkflowExecution.PhaseR\x06phases\x129\n\x05email\x18\x02 \x01(\x0b2!.flyteidl.admin.EmailNotificationH\x00R\x05email\x12F\n\npager_duty\x18\x03 \x01(\x0b2%.flyteidl.admin.PagerDutyNotificationH\x00R\tpagerDuty\x129\n\x05slack\x18\x04 \x01(\x0b2!.flyteidl.admin.SlackNotificationH\x00R\x05slackB\x06\n\x04type"5\n\x07UrlBlob\x12\x10\n\x03url\x18\x01 \x01(\tR\x03url\x12\x14\n\x05bytes\x18\x02 \x01(\x03R\x05bytes:\x02\x18\x01"\x7f\n\x06Labels\x12:\n\x06values\x18\x01 \x03(\x0b2".flyteidl.admin.Labels.ValuesEntryR\x06values\x1a9\n\x0bValuesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x028\x01"\x89\x01\n\x0bAnnotations\x12?\n\x06values\x18\x01 \x03(\x0b2\'.flyteidl.admin.Annotations.ValuesEntryR\x06values\x1a9\n\x0bValuesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x028\x01"z\n\x08AuthRole\x12,\n\x12assumable_iam_role\x18\x01 \x01(\tR\x10assumableIamRole\x12<\n\x1akubernetes_service_account\x18\x02 \x01(\tR\x18kubernetesServiceAccount:\x02\x18\x01"K\n\x13RawOutputDataConfig\x124\n\x16output_location_prefix\x18\x01 \x01(\tR\x14outputLocationPrefix*\\\n\x10NamedEntityState\x12\x17\n\x13NAMED_ENTITY_ACTIVE\x10\x00\x12\x19\n\x15NAMED_ENTITY_ARCHIVED\x10\x01\x12\x14\n\x10SYSTEM_GENERATED\x10\x02B\xb1\x01\n\x12com.flyteidl.adminB\x0bCommonProtoP\x01Z5github.com/flyteorg/flyteidl/gen/pb-go/flyteidl/admin\xa2\x02\x03FAX\xaa\x02\x0eFlyteidl.Admin\xca\x02\x0eFlyteidl\\Admin\xe2\x02\x1aFlyteidl\\Admin\\GPBMetadata\xea\x02\x0fFlyteidl::Adminb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flyteidl.admin.common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x12com.flyteidl.adminB\x0bCommonProtoP\x01Z5github.com/flyteorg/flyteidl/gen/pb-go/flyteidl/admin\xa2\x02\x03FAX\xaa\x02\x0eFlyteidl.Admin\xca\x02\x0eFlyteidl\\Admin\xe2\x02\x1aFlyteidl\\Admin\\GPBMetadata\xea\x02\x0fFlyteidl::Admin'
    _URLBLOB._options = None
    _URLBLOB._serialized_options = b'\x18\x01'
    _LABELS_VALUESENTRY._options = None
    _LABELS_VALUESENTRY._serialized_options = b'8\x01'
    _ANNOTATIONS_VALUESENTRY._options = None
    _ANNOTATIONS_VALUESENTRY._serialized_options = b'8\x01'
    _AUTHROLE._options = None
    _AUTHROLE._serialized_options = b'\x18\x01'
    _NAMEDENTITYSTATE._serialized_start = 2983
    _NAMEDENTITYSTATE._serialized_end = 3075
    _NAMEDENTITYIDENTIFIER._serialized_start = 110
    _NAMEDENTITYIDENTIFIER._serialized_end = 203
    _NAMEDENTITYMETADATA._serialized_start = 205
    _NAMEDENTITYMETADATA._serialized_end = 316
    _NAMEDENTITY._serialized_start = 319
    _NAMEDENTITY._serialized_end = 518
    _SORT._serialized_start = 521
    _SORT._serialized_end = 651
    _SORT_DIRECTION._serialized_start = 609
    _SORT_DIRECTION._serialized_end = 651
    _NAMEDENTITYIDENTIFIERLISTREQUEST._serialized_start = 654
    _NAMEDENTITYIDENTIFIERLISTREQUEST._serialized_end = 855
    _NAMEDENTITYLISTREQUEST._serialized_start = 858
    _NAMEDENTITYLISTREQUEST._serialized_end = 1115
    _NAMEDENTITYIDENTIFIERLIST._serialized_start = 1117
    _NAMEDENTITYIDENTIFIERLIST._serialized_end = 1233
    _NAMEDENTITYLIST._serialized_start = 1235
    _NAMEDENTITYLIST._serialized_end = 1331
    _NAMEDENTITYGETREQUEST._serialized_start = 1334
    _NAMEDENTITYGETREQUEST._serialized_end = 1478
    _NAMEDENTITYUPDATEREQUEST._serialized_start = 1481
    _NAMEDENTITYUPDATEREQUEST._serialized_end = 1693
    _NAMEDENTITYUPDATERESPONSE._serialized_start = 1695
    _NAMEDENTITYUPDATERESPONSE._serialized_end = 1722
    _OBJECTGETREQUEST._serialized_start = 1724
    _OBJECTGETREQUEST._serialized_end = 1785
    _RESOURCELISTREQUEST._serialized_start = 1788
    _RESOURCELISTREQUEST._serialized_end = 1981
    _EMAILNOTIFICATION._serialized_start = 1983
    _EMAILNOTIFICATION._serialized_end = 2045
    _PAGERDUTYNOTIFICATION._serialized_start = 2047
    _PAGERDUTYNOTIFICATION._serialized_end = 2113
    _SLACKNOTIFICATION._serialized_start = 2115
    _SLACKNOTIFICATION._serialized_end = 2177
    _NOTIFICATION._serialized_start = 2180
    _NOTIFICATION._serialized_end = 2456
    _URLBLOB._serialized_start = 2458
    _URLBLOB._serialized_end = 2511
    _LABELS._serialized_start = 2513
    _LABELS._serialized_end = 2640
    _LABELS_VALUESENTRY._serialized_start = 2583
    _LABELS_VALUESENTRY._serialized_end = 2640
    _ANNOTATIONS._serialized_start = 2643
    _ANNOTATIONS._serialized_end = 2780
    _ANNOTATIONS_VALUESENTRY._serialized_start = 2583
    _ANNOTATIONS_VALUESENTRY._serialized_end = 2640
    _AUTHROLE._serialized_start = 2782
    _AUTHROLE._serialized_end = 2904
    _RAWOUTPUTDATACONFIG._serialized_start = 2906
    _RAWOUTPUTDATACONFIG._serialized_end = 2981