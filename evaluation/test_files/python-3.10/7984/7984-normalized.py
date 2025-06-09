def create_las(*, point_format_id=0, file_version=None):
    """ Function to create a new empty las data object

    .. note::

        If you provide both point_format and file_version
        an exception will be raised if they are not compatible

    >>> las = create_las(point_format_id=6,file_version="1.2")
    Traceback (most recent call last):
     ...
    pylas.errors.PylasError: Point format 6 is not compatible with file version 1.2


    If you provide only the point_format the file_version will automatically
    selected for you.

    >>> las = create_las(point_format_id=0)
    >>> las.header.version == '1.2'
    True

    >>> las = create_las(point_format_id=6)
    >>> las.header.version == '1.4'
    True


    Parameters
    ----------
    point_format_id: int
        The point format you want the created file to have

    file_version: str, optional, default=None
        The las version you want the created las to have

    Returns
    -------
    pylas.lasdatas.base.LasBase
       A new las data object

    """
    if file_version is not None:
        dims.raise_if_version_not_compatible_with_fmt(point_format_id, file_version)
    else:
        file_version = dims.min_file_version_for_point_format(point_format_id)
    header = headers.HeaderFactory.new(file_version)
    header.point_format_id = point_format_id
    if file_version >= '1.4':
        return las14.LasData(header=header)
    return las12.LasData(header=header)