def get_port(self):
    """ Return a port to use to talk to this cluster. """
    if len(self.client_nodes) > 0:
        node = self.client_nodes[0]
    else:
        node = self.nodes[0]
    return node.get_port()