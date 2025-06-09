"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from layerapi.api import ids_pb2 as api_dot_ids__pb2
from layerapi.validate import validate_pb2 as validate_dot_validate__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bapi/entity/operations.proto\x12\x03api\x1a\rapi/ids.proto\x1a\x17validate/validate.proto"=\n\rExecutionPlan\x12,\n\noperations\x18\x01 \x03(\x0b2\x0e.api.OperationB\x08\xfaB\x05\x92\x01\x02\x08\x01"t\n\tOperation\x12.\n\nsequential\x18\x01 \x01(\x0b2\x18.api.SequentialOperationH\x00\x12*\n\x08parallel\x18\x02 \x01(\x0b2\x16.api.ParallelOperationH\x00B\x0b\n\toperation"\xc4\x01\n\x13SequentialOperation\x12:\n\x11feature_set_build\x18\x01 \x01(\x0b2\x19.api.UnsupportedOperationB\x02\x18\x01H\x00\x12/\n\x0bmodel_train\x18\x02 \x01(\x0b2\x18.api.ModelTrainOperationH\x00\x123\n\rdataset_build\x18\x04 \x01(\x0b2\x1a.api.DatasetBuildOperationH\x00B\x0b\n\toperation"\xaf\x01\n\x11ParallelOperation\x128\n\x11feature_set_build\x18\x01 \x03(\x0b2\x19.api.UnsupportedOperationB\x02\x18\x01\x12-\n\x0bmodel_train\x18\x02 \x03(\x0b2\x18.api.ModelTrainOperation\x121\n\rdataset_build\x18\x04 \x03(\x0b2\x1a.api.DatasetBuildOperation"\x16\n\x14UnsupportedOperation"X\n\x13ModelTrainOperation\x12-\n\x10model_version_id\x18\x01 \x01(\x0b2\x13.api.ModelVersionId\x12\x12\n\ndependency\x18\x02 \x03(\t"A\n\x15DatasetBuildOperation\x12\x14\n\x0cdataset_name\x18\x01 \x01(\t\x12\x12\n\ndependency\x18\x02 \x03(\tB\x11\n\rcom.layer.apiP\x01b\x06proto3')
_EXECUTIONPLAN = DESCRIPTOR.message_types_by_name['ExecutionPlan']
_OPERATION = DESCRIPTOR.message_types_by_name['Operation']
_SEQUENTIALOPERATION = DESCRIPTOR.message_types_by_name['SequentialOperation']
_PARALLELOPERATION = DESCRIPTOR.message_types_by_name['ParallelOperation']
_UNSUPPORTEDOPERATION = DESCRIPTOR.message_types_by_name['UnsupportedOperation']
_MODELTRAINOPERATION = DESCRIPTOR.message_types_by_name['ModelTrainOperation']
_DATASETBUILDOPERATION = DESCRIPTOR.message_types_by_name['DatasetBuildOperation']
ExecutionPlan = _reflection.GeneratedProtocolMessageType('ExecutionPlan', (_message.Message,), {'DESCRIPTOR': _EXECUTIONPLAN, '__module__': 'api.entity.operations_pb2'})
_sym_db.RegisterMessage(ExecutionPlan)
Operation = _reflection.GeneratedProtocolMessageType('Operation', (_message.Message,), {'DESCRIPTOR': _OPERATION, '__module__': 'api.entity.operations_pb2'})
_sym_db.RegisterMessage(Operation)
SequentialOperation = _reflection.GeneratedProtocolMessageType('SequentialOperation', (_message.Message,), {'DESCRIPTOR': _SEQUENTIALOPERATION, '__module__': 'api.entity.operations_pb2'})
_sym_db.RegisterMessage(SequentialOperation)
ParallelOperation = _reflection.GeneratedProtocolMessageType('ParallelOperation', (_message.Message,), {'DESCRIPTOR': _PARALLELOPERATION, '__module__': 'api.entity.operations_pb2'})
_sym_db.RegisterMessage(ParallelOperation)
UnsupportedOperation = _reflection.GeneratedProtocolMessageType('UnsupportedOperation', (_message.Message,), {'DESCRIPTOR': _UNSUPPORTEDOPERATION, '__module__': 'api.entity.operations_pb2'})
_sym_db.RegisterMessage(UnsupportedOperation)
ModelTrainOperation = _reflection.GeneratedProtocolMessageType('ModelTrainOperation', (_message.Message,), {'DESCRIPTOR': _MODELTRAINOPERATION, '__module__': 'api.entity.operations_pb2'})
_sym_db.RegisterMessage(ModelTrainOperation)
DatasetBuildOperation = _reflection.GeneratedProtocolMessageType('DatasetBuildOperation', (_message.Message,), {'DESCRIPTOR': _DATASETBUILDOPERATION, '__module__': 'api.entity.operations_pb2'})
_sym_db.RegisterMessage(DatasetBuildOperation)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\rcom.layer.apiP\x01'
    _EXECUTIONPLAN.fields_by_name['operations']._options = None
    _EXECUTIONPLAN.fields_by_name['operations']._serialized_options = b'\xfaB\x05\x92\x01\x02\x08\x01'
    _SEQUENTIALOPERATION.fields_by_name['feature_set_build']._options = None
    _SEQUENTIALOPERATION.fields_by_name['feature_set_build']._serialized_options = b'\x18\x01'
    _PARALLELOPERATION.fields_by_name['feature_set_build']._options = None
    _PARALLELOPERATION.fields_by_name['feature_set_build']._serialized_options = b'\x18\x01'
    _EXECUTIONPLAN._serialized_start = 76
    _EXECUTIONPLAN._serialized_end = 137
    _OPERATION._serialized_start = 139
    _OPERATION._serialized_end = 255
    _SEQUENTIALOPERATION._serialized_start = 258
    _SEQUENTIALOPERATION._serialized_end = 454
    _PARALLELOPERATION._serialized_start = 457
    _PARALLELOPERATION._serialized_end = 632
    _UNSUPPORTEDOPERATION._serialized_start = 634
    _UNSUPPORTEDOPERATION._serialized_end = 656
    _MODELTRAINOPERATION._serialized_start = 658
    _MODELTRAINOPERATION._serialized_end = 746
    _DATASETBUILDOPERATION._serialized_start = 748
    _DATASETBUILDOPERATION._serialized_end = 813