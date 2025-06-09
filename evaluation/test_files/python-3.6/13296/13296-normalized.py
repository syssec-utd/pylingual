def _load_attr(name: str, ctx: ast.AST=ast.Load()) -> ast.Attribute:
    """Generate recursive Python Attribute AST nodes for resolving nested
    names."""
    attrs = name.split('.')

    def attr_node(node, idx):
        if idx >= len(attrs):
            node.ctx = ctx
            return node
        return attr_node(ast.Attribute(value=node, attr=attrs[idx], ctx=ast.Load()), idx + 1)
    return attr_node(ast.Name(id=attrs[0], ctx=ast.Load()), 1)