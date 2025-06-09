def visit_unaryop(self, node):
    """Detect TypeErrors for unary operands."""
    for error in node.type_errors():
        self.add_message('invalid-unary-operand-type', args=str(error), node=node)