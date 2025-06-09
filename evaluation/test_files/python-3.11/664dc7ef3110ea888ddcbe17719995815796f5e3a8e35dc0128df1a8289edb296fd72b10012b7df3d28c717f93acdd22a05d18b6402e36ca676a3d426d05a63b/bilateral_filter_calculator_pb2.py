"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
    mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
    mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n=mediapipe/calculators/image/bilateral_filter_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto"\xa7\x01\n BilateralFilterCalculatorOptions\x12\x13\n\x0bsigma_color\x18\x01 \x01(\x02\x12\x13\n\x0bsigma_space\x18\x02 \x01(\x022Y\n\x03ext\x12\x1c.mediapipe.CalculatorOptions\x18\xc1\xef\xf4y \x01(\x0b2+.mediapipe.BilateralFilterCalculatorOptions')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.image.bilateral_filter_calculator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_BILATERALFILTERCALCULATOROPTIONS.extensions_by_name['ext'])
    DESCRIPTOR._options = None
    _BILATERALFILTERCALCULATOROPTIONS._serialized_start = 115
    _BILATERALFILTERCALCULATOROPTIONS._serialized_end = 282