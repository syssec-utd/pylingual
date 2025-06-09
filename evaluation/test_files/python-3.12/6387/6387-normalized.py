def measure_geometry(script):
    """ Compute a set of geometric measures of a mesh/pointcloud.

    Bounding box extents and diagonal, principal axis, thin shell barycenter
    (mesh only), vertex barycenter and quality-weighted barycenter (pointcloud
    only), surface area (mesh only), volume (closed mesh) and Inertia tensor
    Matrix (closed mesh).

    Args:
        script: the mlx.FilterScript object or script filename to write
            the filter to.

    Layer stack:
        No impacts

    MeshLab versions:
        2016.12
        1.3.4BETA

    Bugs:
        Bounding box extents not computed correctly for some volumes
    """
    filter_xml = '  <xmlfilter name="Compute Geometric Measures"/>\n'
    util.write_filter(script, filter_xml)
    if isinstance(script, mlx.FilterScript):
        script.parse_geometry = True
    return None