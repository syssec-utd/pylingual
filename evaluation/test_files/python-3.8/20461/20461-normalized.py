def _bypass_ensure_directory(path, mode=511):
    """Sandbox-bypassing version of ensure_directory()"""
    if not WRITE_SUPPORT:
        raise IOError('"os.mkdir" not supported on this platform.')
    (dirname, filename) = split(path)
    if dirname and filename and (not isdir(dirname)):
        _bypass_ensure_directory(dirname)
        mkdir(dirname, mode)