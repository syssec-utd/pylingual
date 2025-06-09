def remove_descendants_of(self, node):
    """Remove all of the descendant operation nodes of node."""
    if isinstance(node, int):
        warnings.warn('Calling remove_descendants_of() with a node id is deprecated, use a DAGNode instead', DeprecationWarning, 2)
        node = self._id_to_node[node]
    desc = nx.descendants(self._multi_graph, node)
    for desc_node in desc:
        if desc_node.type == 'op':
            self.remove_op_node(desc_node)