from google.protobuf import descriptor as _descriptor
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import enum_type_wrapper
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='terminaltype.proto', package='', syntax='proto3', serialized_options=b'\n\x1dcom.ubtechinc.alpha.programme', serialized_pb=b'\n\x12terminaltype.proto*\xbe\x01\n\x0cTerminalType\x12 \n\x1cTERMINAL_TYPE_ANDROID_MOBILE\x10\x00\x12\x1c\n\x18TERMINAL_TYPE_IOS_MOBILE\x10\x01\x12\x1d\n\x19TERMINAL_TYPE_ANDROID_PAD\x10\x02\x12\x19\n\x15TERMINAL_TYPE_IOS_PAD\x10\x03\x12\x1a\n\x16TERMINAL_TYPE_PC_LOCAL\x10\x04\x12\x18\n\x14TERMINAL_TYPE_PC_WEB\x10\x05B\x1f\n\x1dcom.ubtechinc.alpha.programmeb\x06proto3')
_TERMINALTYPE = _descriptor.EnumDescriptor(name='TerminalType', full_name='TerminalType', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='TERMINAL_TYPE_ANDROID_MOBILE', index=0, number=0, serialized_options=None, type=None), _descriptor.EnumValueDescriptor(name='TERMINAL_TYPE_IOS_MOBILE', index=1, number=1, serialized_options=None, type=None), _descriptor.EnumValueDescriptor(name='TERMINAL_TYPE_ANDROID_PAD', index=2, number=2, serialized_options=None, type=None), _descriptor.EnumValueDescriptor(name='TERMINAL_TYPE_IOS_PAD', index=3, number=3, serialized_options=None, type=None), _descriptor.EnumValueDescriptor(name='TERMINAL_TYPE_PC_LOCAL', index=4, number=4, serialized_options=None, type=None), _descriptor.EnumValueDescriptor(name='TERMINAL_TYPE_PC_WEB', index=5, number=5, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=23, serialized_end=213)
_sym_db.RegisterEnumDescriptor(_TERMINALTYPE)
TerminalType = enum_type_wrapper.EnumTypeWrapper(_TERMINALTYPE)
TERMINAL_TYPE_ANDROID_MOBILE = 0
TERMINAL_TYPE_IOS_MOBILE = 1
TERMINAL_TYPE_ANDROID_PAD = 2
TERMINAL_TYPE_IOS_PAD = 3
TERMINAL_TYPE_PC_LOCAL = 4
TERMINAL_TYPE_PC_WEB = 5
DESCRIPTOR.enum_types_by_name['TerminalType'] = _TERMINALTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
DESCRIPTOR._options = None