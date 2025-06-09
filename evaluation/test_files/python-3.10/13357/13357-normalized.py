def visit_Try(self, node: ast.Try) -> Optional[ast.AST]:
    """Eliminate dead code from except try bodies."""
    new_node = self.generic_visit(node)
    assert isinstance(new_node, ast.Try)
    return ast.copy_location(ast.Try(body=_filter_dead_code(new_node.body), handlers=new_node.handlers, orelse=_filter_dead_code(new_node.orelse), finalbody=_filter_dead_code(new_node.finalbody)), new_node)