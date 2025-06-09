def grow(script, iterations=1):
    """ Grow (dilate, expand) the current set of selected faces

    Args:
        script: the FilterScript object or script filename to write
            the filter to.
        iterations (int): the number of times to grow the selection.

    Layer stack:
        No impacts

    MeshLab versions:
        2016.12
        1.3.4BETA
    """
    filter_xml = '  <filter name="Dilate Selection"/>\n'
    for _ in range(iterations):
        util.write_filter(script, filter_xml)
    return None