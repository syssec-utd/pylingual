def is_bare_exception(self, node):
    """
        Checks if the node is a bare exception name from an except block.

        """
    return isinstance(node, Name) and node.id in self.current_except_names