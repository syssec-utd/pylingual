def _prepare_nodes(self):
    """
        Set auxilliary parameters to every node of the tree.
        """
    self.tree.root.up = None
    self.tree.root.bad_branch = self.tree.root.bad_branch if hasattr(self.tree.root, 'bad_branch') else False
    internal_node_count = 0
    for clade in self.tree.get_nonterminals(order='preorder'):
        internal_node_count += 1
        if clade.name is None:
            clade.name = 'NODE_' + format(self._internal_node_count, '07d')
            self._internal_node_count += 1
        for c in clade.clades:
            if c.is_terminal():
                c.bad_branch = c.bad_branch if hasattr(c, 'bad_branch') else False
            c.up = clade
    for clade in self.tree.get_nonterminals(order='postorder'):
        clade.bad_branch = all([c.bad_branch for c in clade])
    self._calc_dist2root()
    self._internal_node_count = max(internal_node_count, self._internal_node_count)