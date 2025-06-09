def simplify(script, texture=True, faces=25000, target_perc=0.0, quality_thr=0.3, preserve_boundary=False, boundary_weight=1.0, optimal_placement=True, preserve_normal=False, planar_quadric=False, selected=False, extra_tex_coord_weight=1.0, preserve_topology=True, quality_weight=False, autoclean=True):
    """ Simplify a mesh using a Quadric based Edge Collapse Strategy, better
        than clustering but slower. Optionally tries to preserve UV
        parametrization for textured meshes.

    Args:
        script: the FilterScript object or script filename to write
            the filter to.
        texture (bool):
        faces (int): The desired final number of faces
        target_perc (float): If non zero, this parameter specifies the desired
            final size of the mesh as a percentage of the initial mesh size.
        quality_thr (float): Quality threshold for penalizing bad shaped faces.
            The value is in the range [0..1]0 accept any kind of face (no
            penalties), 0.5 penalize faces with quality less than 0.5,
            proportionally to their shape.
        preserve_boundary (bool): The simplification process tries not to
            affect mesh boundaries
        boundary_weight (float): The importance of the boundary during
            simplification. Default (1.0) means that the boundary has the same
            importance of the rest. Values greater than 1.0 raise boundary
            importance and has the effect of removing less vertices on the
            border. Admitted range of values (0,+inf).
        optimal_placement (bool): Each collapsed vertex is placed in the
            position minimizing the quadric error. It can fail (creating bad
            spikes) in case of very flat areas. If disabled edges are collapsed
            onto one of the two original vertices and the final mesh is
            composed by a subset of the original vertices.
        preserve_normal (bool): Try to avoid face flipping effects and try to
            preserve the original orientation of the surface.
        planar_quadric (bool): Add additional simplification constraints that
            improves the quality of the simplification of the planar portion of
            the mesh.
        selected (bool): The simplification is applied only to the selected set
            of faces. Take care of the target number of faces!
        extra_tex_coord_weight (float): Additional weight for each extra
            Texture Coordinates for every (selected) vertex. Ignored if texture
            is False.
        preserve_topology (bool): Avoid all the collapses that should cause a
            topology change in the mesh (like closing holes, squeezing handles,
            etc). If checked the genus of the mesh should stay unchanged.
        quality_weight (bool): Use the Per-Vertex quality as a weighting factor
            for the simplification. The weight is used as a error amplification
            value, so a vertex with a high quality value will not be simplified
            and a portion of the mesh with low quality values will be
            aggressively simplified.
        autoclean (bool): After the simplification an additional set of steps
            is performed to clean the mesh (unreferenced vertices, bad faces,
            etc).

    Layer stack:
        Unchanged; current mesh is simplified in place.

    MeshLab versions:
        2016.12 (different filter name)
        1.3.4BETA
    """
    if texture:
        if isinstance(script, FilterScript) and script.ml_version == '2016.12':
            filter_xml = '  <filter name="Simplification: Quadric Edge Collapse Decimation (with texture)">\n'
        else:
            filter_xml = '  <filter name="Quadric Edge Collapse Decimation (with texture)">\n'
    elif isinstance(script, FilterScript) and script.ml_version == '2016.12':
        filter_xml = '  <filter name="Simplification: Quadric Edge Collapse Decimation">\n'
    else:
        filter_xml = '  <filter name="Quadric Edge Collapse Decimation">\n'
    filter_xml = ''.join([filter_xml, '    <Param name="TargetFaceNum" ', 'value="{:d}" '.format(faces), 'description="Target number of faces" ', 'type="RichInt" ', '/>\n', '    <Param name="TargetPerc" ', 'value="{}" '.format(target_perc), 'description="Percentage reduction (0..1)" ', 'type="RichFloat" ', '/>\n', '    <Param name="QualityThr" ', 'value="{}" '.format(quality_thr), 'description="Quality threshold" ', 'type="RichFloat" ', '/>\n', '    <Param name="PreserveBoundary" ', 'value="{}" '.format(str(preserve_boundary).lower()), 'description="Preserve Boundary of the mesh" ', 'type="RichBool" ', '/>\n', '    <Param name="BoundaryWeight" ', 'value="{}" '.format(boundary_weight), 'description="Boundary Preserving Weight" ', 'type="RichFloat" ', '/>\n', '    <Param name="OptimalPlacement" ', 'value="{}" '.format(str(optimal_placement).lower()), 'description="Optimal position of simplified vertices" ', 'type="RichBool" ', '/>\n', '    <Param name="PreserveNormal" ', 'value="{}" '.format(str(preserve_normal).lower()), 'description="Preserve Normal" ', 'type="RichBool" ', '/>\n', '    <Param name="PlanarQuadric" ', 'value="{}" '.format(str(planar_quadric).lower()), 'description="Planar Simplification" ', 'type="RichBool" ', '/>\n', '    <Param name="Selected" ', 'value="{}" '.format(str(selected).lower()), 'description="Simplify only selected faces" ', 'type="RichBool" ', '/>\n'])
    if texture:
        filter_xml = ''.join([filter_xml, '    <Param name="Extratcoordw" ', 'value="{}" '.format(extra_tex_coord_weight), 'description="Texture Weight" ', 'type="RichFloat" ', '/>\n'])
    else:
        filter_xml = ''.join([filter_xml, '    <Param name="PreserveTopology" ', 'value="{}" '.format(str(preserve_topology).lower()), 'description="Preserve Topology" ', 'type="RichBool" ', '/>\n', '    <Param name="QualityWeight" ', 'value="{}" '.format(str(quality_weight).lower()), 'description="Weighted Simplification" ', 'type="RichBool" ', '/>\n', '    <Param name="AutoClean" ', 'value="{}" '.format(str(autoclean).lower()), 'description="Post-simplification cleaning" ', 'type="RichBool" ', '/>\n'])
    filter_xml = ''.join([filter_xml, '  </filter>\n'])
    util.write_filter(script, filter_xml)
    return None