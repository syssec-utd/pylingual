from pylingual.masking.global_masker import TypeSensitiveDict


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
