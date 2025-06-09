"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
import SessionFolderBasic_pb2 as SessionFolderBasic__pb2
import SessionReference_pb2 as SessionReference__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17SessionFolderInfo.proto\x12!AcFunDanmu.Im.Cloud.SessionFolder\x1a\x18SessionFolderBasic.proto\x1a\x16SessionReference.proto"\xb5\x01\n\x11SessionFolderInfo\x12Q\n\x12sessionFolderBasic\x18\x01 \x01(\x0b25.AcFunDanmu.Im.Cloud.SessionFolder.SessionFolderBasic\x12M\n\x10sessionReference\x18\x02 \x03(\x0b23.AcFunDanmu.Im.Cloud.SessionFolder.SessionReferenceb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'SessionFolderInfo_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _SESSIONFOLDERINFO._serialized_start = 113
    _SESSIONFOLDERINFO._serialized_end = 294