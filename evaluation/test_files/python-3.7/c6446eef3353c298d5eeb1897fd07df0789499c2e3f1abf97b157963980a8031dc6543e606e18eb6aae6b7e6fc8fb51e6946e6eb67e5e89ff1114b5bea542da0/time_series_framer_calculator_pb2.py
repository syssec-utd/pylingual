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
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n?mediapipe/calculators/audio/time_series_framer_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto"\xc5\x03\n!TimeSeriesFramerCalculatorOptions\x12\x1e\n\x16frame_duration_seconds\x18\x01 \x01(\x01\x12 \n\x15frame_overlap_seconds\x18\x02 \x01(\x01:\x010\x12/\n emulate_fractional_frame_overlap\x18\x05 \x01(\x08:\x05false\x12\x1e\n\x10pad_final_packet\x18\x03 \x01(\x08:\x04true\x12Z\n\x0fwindow_function\x18\x04 \x01(\x0e2;.mediapipe.TimeSeriesFramerCalculatorOptions.WindowFunction:\x04NONE\x12"\n\x13use_local_timestamp\x18\x06 \x01(\x08:\x05false"1\n\x0eWindowFunction\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07HAMMING\x10\x01\x12\x08\n\x04HANN\x10\x022Z\n\x03ext\x12\x1c.mediapipe.CalculatorOptions\x18\xc5\xa7\x92\x18 \x01(\x0b2,.mediapipe.TimeSeriesFramerCalculatorOptions')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.audio.time_series_framer_calculator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TIMESERIESFRAMERCALCULATOROPTIONS.extensions_by_name['ext'])
    DESCRIPTOR._options = None
    _TIMESERIESFRAMERCALCULATOROPTIONS._serialized_start = 117
    _TIMESERIESFRAMERCALCULATOROPTIONS._serialized_end = 570
    _TIMESERIESFRAMERCALCULATOROPTIONS_WINDOWFUNCTION._serialized_start = 429
    _TIMESERIESFRAMERCALCULATOROPTIONS_WINDOWFUNCTION._serialized_end = 478