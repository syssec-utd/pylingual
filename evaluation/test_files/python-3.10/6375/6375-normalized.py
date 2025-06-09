def voronoi(script, region_num=10, overlap=False):
    """Voronoi Atlas parameterization

    """
    filter_xml = ''.join(['  <filter name="Parametrization: Voronoi Atlas">\n', '    <Param name="regionNum"', 'value="%d"' % region_num, 'description="Approx. Region Num"', 'type="RichInt"', 'tooltip="An estimation of the number of regions that must be generated. Smaller regions could lead to parametrizations with smaller distortion."', '/>\n', '    <Param name="overlapFlag"', 'value="%s"' % str(overlap).lower(), 'description="Overlap"', 'type="RichBool"', 'tooltip="If checked the resulting parametrization will be composed by overlapping regions, e.g. the resulting mesh will have duplicated faces: each region will have a ring of ovelapping duplicate faces that will ensure that border regions will be parametrized in the atlas twice. This is quite useful for building mipmap robust atlases"', '/>\n', '  </filter>\n'])
    util.write_filter(script, filter_xml)
    return None