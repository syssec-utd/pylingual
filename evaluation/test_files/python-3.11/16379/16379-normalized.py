def add_node(self, node_or_ID, **kwds):
    """ Adds a node to the graph.
        """
    if not isinstance(node_or_ID, Node):
        nodeID = str(node_or_ID)
        if nodeID in self.nodes:
            node = self.nodes[self.nodes.index(nodeID)]
        else:
            if self.default_node is not None:
                node = self.default_node.clone_traits(copy='deep')
                node.ID = nodeID
            else:
                node = Node(nodeID)
            self.nodes.append(node)
    else:
        node = node_or_ID
        if node in self.nodes:
            node = self.nodes[self.nodes.index(node_or_ID)]
        else:
            self.nodes.append(node)
    node.set(**kwds)
    return node