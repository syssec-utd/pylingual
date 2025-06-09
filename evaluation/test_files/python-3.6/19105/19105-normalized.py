def get_tempfile(suffix='.txt', dirpath=None):
    """ Return a temporary file with the given suffix within dirpath.
    If dirpath is None, will look for a temporary folder in your system.

    Parameters
    ----------
    suffix: str
        Temporary file name suffix

    dirpath: str
        Folder path where create the temporary file

    Returns
    -------
    temp_filepath: str
        The path to the temporary path
    """
    if dirpath is None:
        dirpath = get_temp_dir()
    return tempfile.NamedTemporaryFile(suffix=suffix, dir=dirpath)