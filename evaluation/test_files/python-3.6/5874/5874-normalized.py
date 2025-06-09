def _check_logical_tautology(self, node):
    """Check if identifier is compared against itself.
        :param node: Compare node
        :type node: astroid.node_classes.Compare
        :Example:
        val = 786
        if val == val:  # [comparison-with-itself]
            pass
        """
    left_operand = node.left
    right_operand = node.ops[0][1]
    operator = node.ops[0][0]
    if isinstance(left_operand, astroid.Const) and isinstance(right_operand, astroid.Const):
        left_operand = left_operand.value
        right_operand = right_operand.value
    elif isinstance(left_operand, astroid.Name) and isinstance(right_operand, astroid.Name):
        left_operand = left_operand.name
        right_operand = right_operand.name
    if left_operand == right_operand:
        suggestion = '%s %s %s' % (left_operand, operator, right_operand)
        self.add_message('comparison-with-itself', node=node, args=(suggestion,))