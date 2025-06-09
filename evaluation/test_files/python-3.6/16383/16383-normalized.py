def add_edge(self, tail_node_or_ID, head_node_or_ID, **kwds):
    """ Adds an edge to the graph.
        """
    tail_node = self.add_node(tail_node_or_ID)
    head_node = self.add_node(head_node_or_ID)
    if 'directed' in self.trait_names():
        directed = self.directed
    else:
        directed = False
    if self.default_edge is not None:
        edge = self.default_edge.clone_traits(copy='deep')
        edge.tail_node = tail_node
        edge.head_node = head_node
        edge.conn = '->' if directed else '--'
        edge.set(**kwds)
    else:
        edge = Edge(tail_node, head_node, directed, **kwds)
    if 'strict' in self.trait_names():
        if not self.strict:
            self.edges.append(edge)
        else:
            self.edges.append(edge)
    else:
        self.edges.append(edge)