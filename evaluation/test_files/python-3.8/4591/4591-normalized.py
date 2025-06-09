def mkdir_p(newdir, mode=511):
    """The missing mkdir -p functionality in os."""
    try:
        os.makedirs(newdir, mode)
    except OSError as err:
        if err.errno != errno.EEXIST or not os.path.isdir(newdir):
            raise