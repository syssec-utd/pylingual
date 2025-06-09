def depth(self):
    """Return the circuit depth.
        Returns:
            int: the circuit depth
        Raises:
            DAGCircuitError: if not a directed acyclic graph
        """
    if not nx.is_directed_acyclic_graph(self._multi_graph):
        raise DAGCircuitError('not a DAG')
    depth = nx.dag_longest_path_length(self._multi_graph) - 1
    return depth if depth != -1 else 0