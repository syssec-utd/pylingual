def build_top_graph(self, tokens):
    """ Build a Godot graph instance from parsed data.
        """
    strict = tokens[0] == 'strict'
    graphtype = tokens[1]
    directed = graphtype == 'digraph'
    graphname = tokens[2]
    graph = Graph(ID=graphname, strict=strict, directed=directed)
    self.graph = self.build_graph(graph, tokens[3])