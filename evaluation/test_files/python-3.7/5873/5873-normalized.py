def _check_literal_comparison(self, literal, node):
    """Check if we compare to a literal, which is usually what we do not want to do."""
    nodes = (astroid.List, astroid.Tuple, astroid.Dict, astroid.Set)
    is_other_literal = isinstance(literal, nodes)
    is_const = False
    if isinstance(literal, astroid.Const):
        if isinstance(literal.value, bool) or literal.value is None:
            return
        is_const = isinstance(literal.value, (bytes, str, int, float))
    if is_const or is_other_literal:
        self.add_message('literal-comparison', node=node)