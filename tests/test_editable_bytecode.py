import copy
import sys

import pytest
from xdis import get_opcode

from pylingual.editable_bytecode import EditableBytecode
from pylingual.editable_bytecode.EditableBytecode import _encode_name_arg
from pylingual.utils.version import PythonVersion


def _bytecode(source: str) -> EditableBytecode:
    code = compile(source, "<test>", "exec")
    return EditableBytecode(code, get_opcode(sys.version_info[:2], False), sys.version_info[:3])


def test_insert_insts_reencodes_load_global_name_index():
    destination = _bytecode("existing = 0")
    source = _bytecode("def f():\n    return target\n").child_bytecodes[0]
    load_global = copy.copy(next(inst for inst in source.instructions if inst.opname == "LOAD_GLOBAL"))
    original_flags = load_global.arg & 1

    destination.insert_insts({0: [load_global]})

    name_index = destination.co_names.index("target")
    assert load_global.arg == name_index << 1 | original_flags


@pytest.mark.parametrize(
    ("opname", "name_index", "original_arg", "version", "expected"),
    [
        ("LOAD_GLOBAL", 3, 2, (3, 14), 6),
        ("LOAD_GLOBAL", 3, 3, (3, 14), 7),
        ("LOAD_ATTR", 4, 1, (3, 14), 9),
        ("LOAD_SUPER_ATTR", 5, 3, (3, 14), 23),
        ("IMPORT_NAME", 6, 2, (3, 15), 26),
        ("STORE_ATTR", 7, 1, (3, 14), 7),
    ],
)
def test_encode_name_arg_preserves_packed_flags(opname, name_index, original_arg, version, expected):
    assert _encode_name_arg(opname, name_index, original_arg, PythonVersion(version)) == expected
