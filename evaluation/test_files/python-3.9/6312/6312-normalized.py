def snap_mismatched_borders(script, edge_dist_ratio=0.01, unify_vert=True):
    """ Try to snap together adjacent borders that are slightly mismatched.

    This situation can happen on badly triangulated adjacent patches defined by
    high order surfaces. For each border vertex the filter snaps it onto the
    closest boundary edge only if it is closest of edge_legth*threshold. When
    vertex is snapped the corresponding face it split and a new vertex is
    created.

    Args:
        script: the FilterScript object or script filename to write
            the filter to.
        edge_dist_ratio (float): Collapse edge when the edge / distance ratio
            is greater than this value. E.g. for default value 1000 two
            straight border edges are collapsed if the central vertex dist from
            the straight line composed by the two edges less than a 1/1000 of
            the sum of the edges length. Larger values enforce that only
            vertexes very close to the line are removed.
        unify_vert (bool): If true the snap vertices are welded together.

    Layer stack:
        No impacts

    MeshLab versions:
        2016.12
        1.3.4BETA
    """
    filter_xml = ''.join(['  <filter name="Snap Mismatched Borders">\n', '    <Param name="EdgeDistRatio" ', 'value="{}" '.format(edge_dist_ratio), 'description="Edge Distance Ratio" ', 'type="RichFloat" ', '/>\n', '    <Param name="UnifyVertices" ', 'value="{}" '.format(str(unify_vert).lower()), 'description="UnifyVertices" ', 'type="RichBool" ', '/>\n', '  </filter>\n'])
    util.write_filter(script, filter_xml)
    return None