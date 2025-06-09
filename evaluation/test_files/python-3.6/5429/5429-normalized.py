def overrides_a_method(class_node: astroid.node_classes.NodeNG, name: str) -> bool:
    """return True if <name> is a method overridden from an ancestor"""
    for ancestor in class_node.ancestors():
        if name in ancestor and isinstance(ancestor[name], astroid.FunctionDef):
            return True
    return False