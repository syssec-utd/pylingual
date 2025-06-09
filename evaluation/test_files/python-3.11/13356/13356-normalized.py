def visit_While(self, node: ast.While) -> Optional[ast.AST]:
    """Eliminate dead code from while bodies."""
    new_node = self.generic_visit(node)
    assert isinstance(new_node, ast.While)
    return ast.copy_location(ast.While(test=new_node.test, body=_filter_dead_code(new_node.body), orelse=_filter_dead_code(new_node.orelse)), new_node)