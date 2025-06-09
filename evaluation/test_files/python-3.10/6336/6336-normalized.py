def curvature_flipping(script, angle_threshold=1.0, curve_type=0, selected=False):
    """ Use the points and normals to build a surface using the Poisson
        Surface reconstruction approach.

    Args:
        script: the FilterScript object or script filename to write
            the filter to.
        angle_threshold (float): To avoid excessive flipping/swapping we
            consider only couple of faces with a significant diedral angle
            (e.g. greater than the indicated threshold).
        curve_type (int): Choose a metric to compute surface curvature on vertices
            H = mean curv, K = gaussian curv, A = area per vertex
            1: Mean curvature = H
            2: Norm squared mean curvature = (H * H) / A
            3: Absolute curvature:
                if(K >= 0) return 2 * H
                else return 2 * sqrt(H ^ 2 - A * K)

    Layer stack:
        No impacts

    MeshLab versions:
        2016.12
        1.3.4BETA
    """
    filter_xml = ''.join(['  <filter name="Curvature flipping optimization">\n', '    <Param name="selection" ', 'value="{}" '.format(str(selected).lower()), 'description="Update selection" ', 'type="RichBool" ', '/>\n', '    <Param name="pthreshold" ', 'value="{}" '.format(angle_threshold), 'description="Angle Thr (deg)" ', 'type="RichFloat" ', '/>\n', '    <Param name="curvtype" ', 'value="{:d}" '.format(curve_type), 'description="Curvature metric" ', 'enum_val0="mean" ', 'enum_val1="norm squared" ', 'enum_val2="absolute" ', 'enum_cardinality="3" ', 'type="RichEnum" ', '/>\n', '  </filter>\n'])
    util.write_filter(script, filter_xml)
    return None