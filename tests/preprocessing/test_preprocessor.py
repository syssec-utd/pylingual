from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest
from xdis import get_opcode

from pylingual.editable_bytecode import EditableBytecode
from pylingual.preprocessor import Preprocessor

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _extract_container_literals(source: str) -> list:
    tree = ast.parse(source)
    containers = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.List, ast.Set, ast.Tuple, ast.Dict)):
            try:
                val = ast.literal_eval(node)
            except (ValueError, SyntaxError):
                continue
            if val is None:
                continue
            if not hasattr(val, "__len__"):
                continue
            if len(val) == 0:
                continue
            containers.append(val)
    return containers


def _value_in_container(value, container) -> bool:
    if isinstance(container, dict):
        items = list(container.keys()) + list(container.values())
    elif isinstance(container, (list, tuple, set, frozenset)):
        items = list(container)
    else:
        return False
    for item in items:
        if _values_match(value, item):
            return True
        if isinstance(item, (list, tuple, set, frozenset, dict)):
            if _value_in_container(value, item):
                return True
    return False


def _values_match(expected, actual) -> bool:
    if isinstance(expected, frozenset):
        if type(actual) is set and actual == set(expected):
            return True
        if type(actual) is frozenset and actual == expected:
            return True
        return False
    if type(expected) is not type(actual):
        return False
    return expected == actual


def _value_in_co_consts(value, co_consts) -> bool:
    for const in co_consts:
        if _values_match(value, const):
            return True
        if isinstance(const, (list, tuple, set, frozenset, dict)):
            if _value_in_container(value, const):
                return True
    return False


def _preprocess_source(source: str) -> EditableBytecode:
    code = compile(source, "<test>", "exec")
    opc = get_opcode(sys.version_info[:2], False)
    bc = EditableBytecode(code, opc, sys.version_info[:3])
    Preprocessor().preprocess(bc)
    return bc


@pytest.mark.parametrize(
    "fixture",
    sorted(FIXTURES_DIR.glob("*.py")),
    ids=lambda p: p.stem,
)
def test_container_values_in_co_consts(fixture: Path) -> None:
    source = fixture.read_text()
    containers = _extract_container_literals(source)
    if not containers:
        pytest.skip("No non-empty container literals in fixture")

    bc = _preprocess_source(source)

    missing = []
    for value in containers:
        if not _value_in_co_consts(value, bc.co_consts):
            missing.append(value)

    assert not missing, (
        f"{len(missing)} container value(s) not found in co_consts:\n"
        f"  missing: {missing!r}\n"
        f"  co_consts: {bc.co_consts!r}"
    )