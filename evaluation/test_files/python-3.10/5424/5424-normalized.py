def is_defined_before(var_node: astroid.node_classes.NodeNG) -> bool:
    """return True if the variable node is defined by a parent node (list,
    set, dict, or generator comprehension, lambda) or in a previous sibling
    node on the same line (statement_defining ; statement_using)
    """
    varname = var_node.name
    _node = var_node.parent
    while _node:
        if is_defined_in_scope(var_node, varname, _node):
            return True
        _node = _node.parent
    stmt = var_node.statement()
    _node = stmt.previous_sibling()
    lineno = stmt.fromlineno
    while _node and _node.fromlineno == lineno:
        for assign_node in _node.nodes_of_class(astroid.AssignName):
            if assign_node.name == varname:
                return True
        for imp_node in _node.nodes_of_class((astroid.ImportFrom, astroid.Import)):
            if varname in [name[1] or name[0] for name in imp_node.names]:
                return True
        _node = _node.previous_sibling()
    return False