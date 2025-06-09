def data_filename(fname, pkgdir=''):
    """Return the path to a data file of ours.

    The file is searched for on `STATIC_PATH`, and the first place it's found,
    is returned.

    Each directory in `STATIC_PATH` is searched as-is, and also, if `pkgdir`
    is provided, at that subdirectory.

    """
    for static_dir in STATIC_PATH:
        static_filename = os.path.join(static_dir, fname)
        if os.path.exists(static_filename):
            return static_filename
        if pkgdir:
            static_filename = os.path.join(static_dir, pkgdir, fname)
            if os.path.exists(static_filename):
                return static_filename
    raise CoverageException("Couldn't find static file %r" % fname)