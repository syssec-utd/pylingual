def _set_node_lists(self, new):
    """ Maintains each edge's list of available nodes.
        """
    for edge in self.edges:
        edge._nodes = self.nodes