def mkdirs(path, mode):
    """
    Creates the directory specified by path, creating intermediate directories
    as necessary. If directory already exists, this is a no-op.

    :param path: The directory to create
    :type path: str
    :param mode: The mode to give to the directory e.g. 0o755, ignores umask
    :type mode: int
    """
    try:
        o_umask = os.umask(0)
        os.makedirs(path, mode)
    except OSError:
        if not os.path.isdir(path):
            raise
    finally:
        os.umask(o_umask)