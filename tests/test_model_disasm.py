import py_compile
import runpy

import pytest

from pylingual.editable_bytecode import PYCFile
from pylingual.masking.global_masker import Masker
from pylingual.masking.model_disasm import create_global_masker, mask_source, restore_masked_source, restore_masked_source_text


@pytest.mark.parametrize("mask", ["<mask_0>", "'<mask_0>'", '"<mask_0>"'])
def test_container_masks_restore_without_wrapper_quotes(mask):
    masker = Masker()
    masker.global_tab[{"size": (32, 32), "crop": True}] = "<mask_0>"

    assert restore_masked_source_text([f"value = {mask}"], masker) == ["value = {'size': (32, 32), 'crop': True}"]


def test_quoted_string_mask_keeps_literal_quotes():
    masker = Masker()
    masker.global_tab["it's"] = "<mask_0>"

    assert restore_masked_source_text(["value = '<mask_0>'"], masker) == ["value = 'it\\'s'"]


def test_container_mask_before_closing_brace_is_not_escaped():
    masker = Masker()
    masker.global_tab[{"size": (32, 32), "crop": True}] = "<mask_0>"

    source = "value = {'first': <mask_0>, 'last': <mask_0>}"
    expected = "value = {'first': {'size': (32, 32), 'crop': True}, 'last': {'size': (32, 32), 'crop': True}}"

    assert restore_masked_source_text([source], masker) == [expected]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ([slice(None)], ":"),
        ([slice(1, None)], "1:"),
        ([slice(None, 5)], ":5"),
        ([slice(None, None, -1)], "::(-1)"),
        ([slice(None), None], ":, None"),
    ],
)
def test_slice_container_masks_restore_as_subscript_syntax(value, expected):
    masker = Masker()
    masker.global_tab[value] = "<mask_0>"

    source = "value = array[<mask_0>, *tail]"

    assert restore_masked_source_text([source], masker) == [f"value = array[{expected}, *tail]"]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (([0], ...), "[0], ..."),
        ((['nominal'], ...), "['nominal'], ..."),
        ((slice(None), ...), ":, ..."),
        ((1, ...), "1, ..."),
    ],
)
def test_ellipsis_subscript_tuple_masks_restore_as_subscript_syntax(value, expected):
    # A folded subscript tuple containing Ellipsis must restore as comma-joined
    # subscript syntax (x[[0], ...]) rather than the repr (x[([0], Ellipsis)]) which
    # recompiles to LOAD_NAME Ellipsis instead of LOAD_CONST Ellipsis.
    masker = Masker()
    masker.global_tab[value] = "<mask_0>"
    source = "value = array[<mask_0>]"
    assert restore_masked_source_text([source], masker) == [f"value = array[{expected}]"]


def test_string_masks_between_format_placeholders_are_escaped():
    # 3.14 folds `'...%s...' % args` into BUILD_STRING, so a single literal holds several masks
    # and the middle ones touch neither quote
    masker = Masker()
    masker.global_tab["Invalid '"] = "<mask_0>"
    masker.global_tab["', must be in "] = "<mask_1>"

    source = "error += '<mask_0>%s<mask_1>%s' % (sort, sorts)"

    assert restore_masked_source_text([source], masker) == ["error += 'Invalid \\'%s\\', must be in %s' % (sort, sorts)"]


def test_bytes_mask_next_to_brace_is_not_escaped():
    masker = Masker()
    masker.global_tab[b"\x00"] = "<mask_0>"

    assert restore_masked_source_text(["value = {<mask_0>: 1}"], masker) == ["value = {b'\\x00': 1}"]


def test_string_mask_in_fstring_replacement_field():
    masker = Masker()
    masker.global_tab["it's"] = "<mask_0>"
    masker.global_tab["name"] = "<mask_1>"

    source = "value = f'{<mask_1>}<mask_0>{<mask_1>[\"<mask_0>\"]}'"

    assert restore_masked_source_text([source], masker) == ["value = f'{name}it\\'s{name[\"it\\'s\"]}'"]


def test_string_mask_in_fstring_literal_doubles_braces():
    masker = Masker()
    masker.global_tab["{"] = "<mask_0>"
    masker.global_tab["}"] = "<mask_1>"
    masker.global_tab["var"] = "<mask_2>"

    source = "value = f'<mask_0>{<mask_2>}<mask_1>' + '<mask_0>'"

    assert restore_masked_source_text([source], masker) == ["value = f'{{{var}}}' + '{'"]


@pytest.mark.parametrize("text", ["", "value = <mask_0>", "value = <mask_0>\n", "value = <mask_0>\n\nother = <mask_0>"])
def test_restore_masked_source_file_wrapper(tmp_path, text):
    masker = Masker()
    masker.global_tab["secret"] = "<mask_0>"
    masked_file = tmp_path / "masked.py"
    masked_file.write_text(text)

    restored = restore_masked_source(masked_file, masker, (3, 13))
    assert restored == "\n".join(restore_masked_source_text(text.splitlines(), masker))
    assert isinstance(restored, str)


@pytest.mark.parametrize("source", ["result = 42\n", "result = 'hello'\n", "values = [2, 3]\nresult = values[0] + values[1]\n"])
def test_restore_masked_source_file_wrapper_pyc_round_trip(tmp_path, source):
    original = tmp_path / "original.py"
    original.write_text(source)
    original_pyc = tmp_path / "original.pyc"
    py_compile.compile(str(original), cfile=str(original_pyc), doraise=True)
    masker = create_global_masker(PYCFile(original_pyc))
    masked = tmp_path / "masked.py"
    masked.write_text(mask_source(original, masker, masker.version))

    restored = tmp_path / "restored.py"
    restored.write_text(restore_masked_source(masked, masker, masker.version))
    restored_pyc = tmp_path / "restored.pyc"
    py_compile.compile(str(restored), cfile=str(restored_pyc), doraise=True)

    assert runpy.run_path(str(restored_pyc))["result"] == runpy.run_path(str(original_pyc))["result"]
