def to_polycollection(self, *args, **kwargs):
    """
    Returns the mesh as matplotlib polygon collection. (tested only for 2D meshes)
    """
    from matplotlib import collections
    (nodes, elements) = (self.nodes, self.elements.reset_index())
    verts = []
    index = []
    for (etype, group) in elements.groupby([('type', 'argiope', '')]):
        index += list(group.index)
        nvert = ELEMENTS[etype].nvert
        conn = group.conn.values[:, :nvert].flatten()
        coords = nodes.coords[['x', 'y']].loc[conn].values.reshape(len(group), nvert, 2)
        verts += list(coords)
    verts = np.array(verts)
    verts = verts[np.argsort(index)]
    return collections.PolyCollection(verts, *args, **kwargs)