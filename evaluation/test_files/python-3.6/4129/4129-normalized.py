def remove_all_ops_named(self, opname):
    """Remove all operation nodes with the given name."""
    for n in self.named_nodes(opname):
        self.remove_op_node(n)