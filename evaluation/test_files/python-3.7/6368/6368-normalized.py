def duplicate_verts(script):
    """ "Check for every vertex on the mesh: if there are two vertices with
        the same coordinates they are merged into a single one.

    Args:
        script: the FilterScript object or script filename to write
            the filter to.

    Layer stack:
        No impacts

    MeshLab versions:
        2016.12
        1.3.4BETA
    """
    if script.ml_version == '1.3.4BETA':
        filter_xml = '  <filter name="Remove Duplicated Vertex"/>\n'
    else:
        filter_xml = '  <filter name="Remove Duplicate Vertices"/>\n'
    util.write_filter(script, filter_xml)
    return None