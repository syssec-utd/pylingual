def multigraph_layers(self):
    """Yield layers of the multigraph."""
    predecessor_count = dict()
    cur_layer = [node for node in self.input_map.values()]
    yield cur_layer
    next_layer = []
    while cur_layer:
        for node in cur_layer:
            for successor in self._multi_graph.successors(node):
                multiplicity = self._multi_graph.number_of_edges(node, successor)
                if successor in predecessor_count:
                    predecessor_count[successor] -= multiplicity
                else:
                    predecessor_count[successor] = self._multi_graph.in_degree(successor) - multiplicity
                if predecessor_count[successor] == 0:
                    next_layer.append(successor)
                    del predecessor_count[successor]
        yield next_layer
        cur_layer = next_layer
        next_layer = []