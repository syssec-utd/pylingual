def node_type(node: astroid.node_classes.NodeNG) -> Optional[type]:
    """Return the inferred type for `node`

    If there is more than one possible type, or if inferred type is Uninferable or None,
    return None
    """
    types = set()
    try:
        for var_type in node.infer():
            if var_type == astroid.Uninferable or is_none(var_type):
                continue
            types.add(var_type)
            if len(types) > 1:
                return None
    except astroid.InferenceError:
        return None
    return types.pop() if types else None