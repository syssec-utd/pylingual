def visit_unaryop(self, node):
    """`not len(S)` must become `not S` regardless if the parent block
        is a test condition or something else (boolean expression)
        e.g. `if not len(S):`"""
    if isinstance(node, astroid.UnaryOp) and node.op == 'not' and _is_len_call(node.operand):
        self.add_message('len-as-condition', node=node)