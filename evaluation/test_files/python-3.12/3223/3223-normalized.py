def _graphviz(self, dot=None):
    """Return a graphviz.Digraph object with a graph of all virtual columns"""
    from graphviz import Digraph
    dot = dot or Digraph(comment='whole dataframe')
    root_nodes = self._root_nodes()
    for column in root_nodes:
        self[column]._graphviz(dot=dot)
    return dot