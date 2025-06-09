def get_cycles(graph_dict, vertices=None):
    """given a dictionary representing an ordered graph (i.e. key are vertices
    and values is a list of destination vertices representing edges), return a
    list of detected cycles
    """
    if not graph_dict:
        return ()
    result = []
    if vertices is None:
        vertices = graph_dict.keys()
    for vertice in vertices:
        _get_cycles(graph_dict, [], set(), result, vertice)
    return result