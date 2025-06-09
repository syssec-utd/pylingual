def insert_child(self, object, index, child):
    """ Inserts a child into the object's children.
        """
    if isinstance(child, Subgraph):
        object.subgraphs.insert(index, child)
    elif isinstance(child, Cluster):
        object.clusters.insert(index, child)
    elif isinstance(child, Node):
        object.nodes.insert(index, child)
    elif isinstance(child, Edge):
        object.edges.insert(index, child)
    else:
        pass