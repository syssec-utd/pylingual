def visit_unaryop(self, node):
    """check use of the non-existent ++ and -- operator operator"""
    if node.op in '+-' and isinstance(node.operand, astroid.UnaryOp) and (node.operand.op == node.op):
        self.add_message('nonexistent-operator', node=node, args=node.op * 2)