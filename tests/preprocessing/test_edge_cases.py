from __future__ import annotations

import sys
from types import SimpleNamespace

import pytest
from xdis import get_opcode

from pylingual.editable_bytecode import EditableBytecode
from pylingual.preprocessor import Preprocessor
from pylingual.preprocessor.container_recovery.utils import _resolve_common_constant


def _preprocess(source: str) -> EditableBytecode:
    code = compile(source, "<test>", "exec")
    opc = get_opcode(sys.version_info[:2], False)
    bc = EditableBytecode(code, opc, sys.version_info[:3])
    Preprocessor().preprocess(bc)
    return bc


def _co_const_values(bc: EditableBytecode) -> list:
    return [c for c in bc.co_consts if isinstance(c, (list, tuple, set, frozenset, dict))]


def test_empty_containers_not_added_by_preprocessor():
    code = compile("a = {}\nb = []\nc = ()\n", "<test>", "exec")
    opc = get_opcode(sys.version_info[:2], False)
    bc = EditableBytecode(code, opc, sys.version_info[:3])
    before = [c for c in bc.co_consts if isinstance(c, (list, tuple, set, frozenset, dict))]
    Preprocessor().preprocess(bc)
    after = [c for c in bc.co_consts if isinstance(c, (list, tuple, set, frozenset, dict))]
    assert after == before, f"Preprocessor added empty containers: before={before!r}, after={after!r}"


def test_falsy_non_empty_list_in_co_consts():
    bc = _preprocess("a = [0]\n")
    values = _co_const_values(bc)
    assert [0] in values, f"[0] not in co_consts values {values!r}"


def test_falsy_non_empty_dict_in_co_consts():
    bc = _preprocess("a = {0: 0}\n")
    values = _co_const_values(bc)
    assert {0: 0} in values, f"{{0: 0}} not in co_consts values {values!r}"


def test_falsy_non_empty_tuple_in_co_consts():
    bc = _preprocess("a = (0,)\n")
    values = _co_const_values(bc)
    assert (0,) in values, f"(0,) not in co_consts values {values!r}"


def test_falsy_non_empty_set_in_co_consts():
    bc = _preprocess("a = {0}\n")
    values = _co_const_values(bc)
    assert any(type(v) is set and v == {0} for v in values), f"{{0}} not in co_consts values {values!r}"


def test_set_recovered_from_frozenset():
    bc = _preprocess("a = {1, 2, 3}\n")
    values = _co_const_values(bc)
    sets = [v for v in values if type(v) is set]
    assert any(v == {1, 2, 3} for v in sets), f"set {{1,2,3}} not in {values!r}"


def test_nested_containers_in_co_consts():
    bc = _preprocess("a = [[1, 2], [3, 4]]\n")
    values = _co_const_values(bc)
    assert [[1, 2], [3, 4]] in values, f"[[1,2],[3,4]] not in co_consts values {values!r}"


def test_deeply_nested_containers():
    bc = _preprocess("a = {'x': [1, {'y': (2, 3)}]}\n")
    values = _co_const_values(bc)
    assert {'x': [1, {'y': (2, 3)}]} in values, f"nested dict not in co_consts values {values!r}"


def test_multiple_containers_same_type():
    bc = _preprocess("a = [1, 2]\nb = [3, 4]\nc = [5, 6]\n")
    values = _co_const_values(bc)
    assert [1, 2] in values, f"[1,2] not in {values!r}"
    assert [3, 4] in values, f"[3,4] not in {values!r}"
    assert [5, 6] in values, f"[5,6] not in {values!r}"


def test_dedup_identical_containers():
    bc = _preprocess("a = [1, 2, 3]\nb = [1, 2, 3]\n")
    values = _co_const_values(bc)
    count = sum(1 for v in values if type(v) is list and v == [1, 2, 3])
    assert count == 1, f"Expected 1 deduplicated [1,2,3], got {count} in {values!r}"


def test_no_dedup_different_type_same_value():
    bc = _preprocess("a = (1, 2)\nb = [1, 2]\n")
    values = _co_const_values(bc)
    tuples = [v for v in values if type(v) is tuple and v == (1, 2)]
    lists = [v for v in values if type(v) is list and v == [1, 2]]
    assert len(tuples) == 1, f"Expected 1 tuple (1,2), got {tuples!r}"
    assert len(lists) == 1, f"Expected 1 list [1,2], got {lists!r}"


def test_preprocessor_rebases_exception_table_offsets():
    code = compile(
        "def f():\n"
        "    try:\n"
        "        value = {'a': 1, 'b': 2, 'c': 3}\n"
        "    finally:\n"
        "        value = None\n",
        "<test>",
        "exec",
    )
    root = EditableBytecode(code, get_opcode(sys.version_info[:2], False), sys.version_info[:3])
    bc = root.bytecode_lookup["f"]
    targets = [bc.get_by_offset(entry.target) for entry in bc.named_exception_table]

    Preprocessor().preprocess(root)

    assert [entry.target for entry in bc.named_exception_table] == [target.offset for target in targets]
    assert all(
        entry.start in bc.offsets and entry.end in bc.offsets and entry.target in bc.offsets
        for entry in bc.named_exception_table
    )


@pytest.mark.parametrize(
    ("arg", "argrepr", "expected"),
    [(0, "AssertionError", AssertionError), (7, "None", None), (9, "True", True), (10, "False", False), (11, "-1", -1)],
)
def test_resolve_raw_common_constant(arg, argrepr, expected):
    instr = SimpleNamespace(arg=arg, argval=arg, argrepr=argrepr)

    assert _resolve_common_constant(instr) is expected


def test_preserve_xdis_resolved_common_constant():
    instr = SimpleNamespace(arg=9, argval=True, argrepr="True")

    assert _resolve_common_constant(instr) is True
