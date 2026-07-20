from __future__ import annotations

import sys
from types import SimpleNamespace

from xdis import get_opcode

from pylingual.editable_bytecode import EditableBytecode
from pylingual.masking.global_masker import Masker, TypeSensitiveDict
from pylingual.masking.model_disasm import create_global_masker
from pylingual.preprocessor import Preprocessor
from pylingual.preprocessor.preprocessor import _make_function_stack_effect


def _preprocess(source: str) -> EditableBytecode:
    code = compile(source, "<test>", "exec")
    opc = get_opcode(sys.version_info[:2], False)
    bytecode = EditableBytecode(code, opc, sys.version_info[:3])
    Preprocessor().preprocess(bytecode)
    return bytecode


def test_positional_default_tuple_shape_remains_visible_to_model():
    bytecode = _preprocess(
        "def f(first=None, second=None, third=None, fourth=None):\n"
        "    pass\n"
    )
    masker = create_global_masker(bytecode)
    defaults = next(
        inst
        for inst in bytecode.instructions
        if inst.opname == "LOAD_CONST" and inst.argval == (None, None, None, None)
    )

    assert masker.get_model_view(defaults) == "LOAD_CONST , (None, None, None, None)"


def test_keyword_only_default_mapping_remains_visible_to_model():
    bytecode = _preprocess(
        "def f(*, retries=3, timeout=30):\n"
        "    pass\n"
    )

    assert any(inst.opname in ("BUILD_CONST_KEY_MAP", "BUILD_MAP") for inst in bytecode.instructions)
    assert not any(inst.opname == "LOAD_CONST" and isinstance(inst.argval, dict) for inst in bytecode.instructions)

    masker = create_global_masker(bytecode)
    keys = next((
        inst
        for inst in bytecode.instructions
        if inst.opname == "LOAD_CONST" and inst.argval == ("retries", "timeout")
    ), None)
    if keys is not None:
        assert masker.get_model_view(keys).startswith("LOAD_CONST , (")


def test_inner_container_still_folds_before_unrelated_make_function():
    bytecode = _preprocess("value = ([1, 2], lambda: 0)\n")

    assert any(
        inst.opname == "LOAD_CONST"
        and inst.argval == [1, 2]
        and getattr(inst, "preprocessed_container", False)
        for inst in bytecode.instructions
    )


def test_call_function_kw_pads_positional_arguments():
    table = TypeSensitiveDict()
    table["opts"] = "<mask_1>"
    table["typ"] = "<mask_2>"
    bytecode = SimpleNamespace(
        version=(3, 6),
        named_exception_table=None,
        opcode=SimpleNamespace(MAKE_FUNCTION=-1),
        resolve_namespace=lambda value: value,
    )
    inst = SimpleNamespace(
        argval=("opts", "typ"),
        bytecode=bytecode,
        has_arg=True,
        is_jump_target=False,
        next_instructions=[SimpleNamespace(opname="CALL_FUNCTION_KW", argval=4)],
        opcode=100,
        opname="LOAD_CONST",
        optype="const",
    )

    assert Masker(table).get_model_view(inst) == (
        "LOAD_CONST , (<KWARG_PAD>, <KWARG_PAD>, '<mask_1>', '<mask_2>')"
    )


def test_pre311_make_function_effect_includes_qualname():
    assert _make_function_stack_effect(0b1110, (3, 6)) == -4
    assert _make_function_stack_effect(0b1110, (3, 12)) == -3
