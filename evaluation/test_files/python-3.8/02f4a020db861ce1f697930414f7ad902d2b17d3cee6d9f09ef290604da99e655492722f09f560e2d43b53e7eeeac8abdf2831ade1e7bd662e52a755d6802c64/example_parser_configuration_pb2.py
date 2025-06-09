"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from tensorflow.core.framework import tensor_pb2 as tensorflow_dot_core_dot_framework_dot_tensor__pb2
from tensorflow.core.framework import tensor_shape_pb2 as tensorflow_dot_core_dot_framework_dot_tensor__shape__pb2
from tensorflow.core.framework import types_pb2 as tensorflow_dot_core_dot_framework_dot_types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n:tensorflow/core/example/example_parser_configuration.proto\x12\ntensorflow\x1a&tensorflow/core/framework/tensor.proto\x1a,tensorflow/core/framework/tensor_shape.proto\x1a%tensorflow/core/framework/types.proto"\xa3\x01\n\x12VarLenFeatureProto\x12#\n\x05dtype\x18\x01 \x01(\x0e2\x14.tensorflow.DataType\x12!\n\x19values_output_tensor_name\x18\x02 \x01(\t\x12"\n\x1aindices_output_tensor_name\x18\x03 \x01(\t\x12!\n\x19shapes_output_tensor_name\x18\x04 \x01(\t"\xbb\x01\n\x14FixedLenFeatureProto\x12#\n\x05dtype\x18\x01 \x01(\x0e2\x14.tensorflow.DataType\x12+\n\x05shape\x18\x02 \x01(\x0b2\x1c.tensorflow.TensorShapeProto\x12.\n\rdefault_value\x18\x03 \x01(\x0b2\x17.tensorflow.TensorProto\x12!\n\x19values_output_tensor_name\x18\x04 \x01(\t"\x9a\x01\n\x14FeatureConfiguration\x12=\n\x11fixed_len_feature\x18\x01 \x01(\x0b2 .tensorflow.FixedLenFeatureProtoH\x00\x129\n\x0fvar_len_feature\x18\x02 \x01(\x0b2\x1e.tensorflow.VarLenFeatureProtoH\x00B\x08\n\x06config"\xbe\x01\n\x1aExampleParserConfiguration\x12K\n\x0bfeature_map\x18\x01 \x03(\x0b26.tensorflow.ExampleParserConfiguration.FeatureMapEntry\x1aS\n\x0fFeatureMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12/\n\x05value\x18\x02 \x01(\x0b2 .tensorflow.FeatureConfiguration:\x028\x01B\xa2\x01\n\x16org.tensorflow.exampleB ExampleParserConfigurationProtosP\x01Zagithub.com/tensorflow/tensorflow/tensorflow/go/core/example/example_parser_configuration_go_proto\xf8\x01\x01b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tensorflow.core.example.example_parser_configuration_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16org.tensorflow.exampleB ExampleParserConfigurationProtosP\x01Zagithub.com/tensorflow/tensorflow/tensorflow/go/core/example/example_parser_configuration_go_proto\xf8\x01\x01'
    _EXAMPLEPARSERCONFIGURATION_FEATUREMAPENTRY._options = None
    _EXAMPLEPARSERCONFIGURATION_FEATUREMAPENTRY._serialized_options = b'8\x01'
    _VARLENFEATUREPROTO._serialized_start = 200
    _VARLENFEATUREPROTO._serialized_end = 363
    _FIXEDLENFEATUREPROTO._serialized_start = 366
    _FIXEDLENFEATUREPROTO._serialized_end = 553
    _FEATURECONFIGURATION._serialized_start = 556
    _FEATURECONFIGURATION._serialized_end = 710
    _EXAMPLEPARSERCONFIGURATION._serialized_start = 713
    _EXAMPLEPARSERCONFIGURATION._serialized_end = 903
    _EXAMPLEPARSERCONFIGURATION_FEATUREMAPENTRY._serialized_start = 820
    _EXAMPLEPARSERCONFIGURATION_FEATUREMAPENTRY._serialized_end = 903