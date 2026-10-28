import ast
import py_compile
import runpy

import pytest

from pylingual.editable_bytecode import PYCFile
from pylingual.masking.global_masker import TypeSensitiveDict
from pylingual.masking.model_disasm import create_global_masker, mask_source


@pytest.mark.parametrize("expression", ["1 << -1", "1 >> -1", "(2 + 3) << -(1 + 1)"])
def test_negative_shift_does_not_crash_source_masking(tmp_path, expression):
    from pylingual.masking.model_disasm import restore_masked_source_text

    source = f"result = {expression}\n"
    path = tmp_path / "shift.py"
    path.write_text(source)
    original_pyc = tmp_path / "shift.pyc"
    py_compile.compile(str(path), cfile=str(original_pyc), doraise=True)
    bc = PYCFile(original_pyc)
    masker = create_global_masker(bc)
    masked = mask_source(path, masker, masker.version)
    restored = "\n".join(restore_masked_source_text(masked.splitlines(), masker))
    assert any(isinstance(n, (ast.LShift, ast.RShift)) for n in ast.walk(ast.parse(restored)))
    restored_path = tmp_path / "restored.py"
    restored_path.write_text(restored)
    restored_pyc = tmp_path / "restored.pyc"
    py_compile.compile(str(restored_path), cfile=str(restored_pyc), doraise=True)
    for pyc_path in (original_pyc, restored_pyc):
        with pytest.raises(ValueError, match="negative shift count"):
            runpy.run_path(str(pyc_path))


def test_equal_sets_share_a_type_sensitive_key_regardless_of_order():
    values = [
        "restore_selector_state",
        "restore_tree_expansions",
        "create_nodes",
        "restore_runtime_state",
        "build_tree.descendants_init",
        "build_tree.root_lookup",
        "create_state_resolver",
        "build_tree.tree_construct",
        "create_state_handles",
        "link_nodes",
        "build_tree.populate_descendants",
        "restore_node_runtime_state",
        "build_tree.group_nodes_by_depth",
        "create_runtime",
        "validate_payload",
        "build_tree",
        "assemble_runtime_dependencies",
    ]
    original = set(values)
    reordered = set(reversed(values))
    table = TypeSensitiveDict()

    table[original] = "<mask_0>"

    assert table[reordered] == "<mask_0>"
    assert reordered in table


def test_equal_nested_containers_share_a_type_sensitive_key():
    original = {"phases": {"load", "build"}, "counts": [1, 2]}
    reordered = {"counts": [1, 2], "phases": {"build", "load"}}
    table = TypeSensitiveDict()

    table[original] = "<mask_0>"

    assert table[reordered] == "<mask_0>"


def test_container_keys_retain_the_original_object_for_iteration():
    original = {"load", "build"}
    table = TypeSensitiveDict()

    table[original] = "<mask_0>"

    assert table.keys() == [original]
    assert list(table.items()) == [(original, "<mask_0>")]
