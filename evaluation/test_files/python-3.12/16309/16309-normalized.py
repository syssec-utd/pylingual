def _get_all_graphs(self):
    """ Property getter.
        """
    top_graph = self

    def get_subgraphs(graph):
        assert isinstance(graph, BaseGraph)
        subgraphs = graph.subgraphs[:]
        for subgraph in graph.subgraphs:
            subsubgraphs = get_subgraphs(subgraph)
            subgraphs.extend(subsubgraphs)
        return subgraphs
    subgraphs = get_subgraphs(top_graph)
    return [top_graph] + subgraphs