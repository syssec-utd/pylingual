def merge_las(*las_files):
    """ Merges multiple las files into one

    merged = merge_las(las_1, las_2)
    merged = merge_las([las_1, las_2, las_3])

    Parameters
    ----------
    las_files: Iterable of LasData or LasData

    Returns
    -------
    pylas.lasdatas.base.LasBase
        The result of the merging

    """
    if len(las_files) == 1:
        las_files = las_files[0]
    if not las_files:
        raise ValueError('No files to merge')
    if not utils.files_have_same_dtype(las_files):
        raise ValueError('All files must have the same point format')
    header = las_files[0].header
    num_pts_merged = sum((len(las.points) for las in las_files))
    merged = create_from_header(header)
    for (dim_name, dim_type) in las_files[0].points_data.point_format.extra_dims:
        merged.add_extra_dim(dim_name, dim_type)
    merged.points = np.zeros(num_pts_merged, merged.points.dtype)
    merged_x = np.zeros(num_pts_merged, np.float64)
    merged_y = np.zeros(num_pts_merged, np.float64)
    merged_z = np.zeros(num_pts_merged, np.float64)
    offset = 0
    for (i, las) in enumerate(las_files, start=1):
        slc = slice(offset, offset + len(las.points))
        merged.points[slc] = las.points
        merged_x[slc] = las.x
        merged_y[slc] = las.y
        merged_z[slc] = las.z
        merged['point_source_id'][slc] = i
        offset += len(las.points)
    merged.x = merged_x
    merged.y = merged_y
    merged.z = merged_z
    return merged