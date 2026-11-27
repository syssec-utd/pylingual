import sys

from xdis import get_opcode, iscode

from pylingual.editable_bytecode import EditableBytecode
from pylingual.masking.global_masker import TypeSensitiveDict
from pylingual.masking.model_disasm import create_global_masker

MASKED_PROGRAM = (
    "def outer():\n"
    "    def inner():\n"
    "        return 1\n"
    "    return inner\n"
    "\n"
    "class Widget:\n"
    "    def method(self):\n"
    "        return 2\n"
)


def _bytecode(source: str) -> EditableBytecode:
    code = compile(source, "<test>", "exec")
    return EditableBytecode(code, get_opcode(sys.version_info[:2], False), sys.version_info[:3])


def _mask_indices(masker) -> list[int]:
    return sorted(int(mask[len("<mask_") : -1]) for mask in masker.global_tab.values())


def test_create_global_masker_interns_nested_code_object_names_not_code_objects():
    bytecode = _bytecode(MASKED_PROGRAM)
    assert any(iscode(getattr(const, "codeobj", const)) for bc in bytecode.iter_bytecodes() for const in bc.co_consts)

    masker = create_global_masker(bytecode)

    assert not any(iscode(getattr(value, "codeobj", value)) for value in masker.global_tab.keys())
    for name in ("outer", "inner", "Widget", "method"):
        assert name in masker.global_tab
        assert masker.global_tab[name].startswith("<mask_")


def test_create_global_masker_never_reassigns_an_existing_mask():
    masker = create_global_masker(_bytecode(MASKED_PROGRAM))

    # every mask slot is used exactly once; overwriting a co_name entry would leave a gap
    assert _mask_indices(masker) == list(range(len(masker.global_tab)))


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
