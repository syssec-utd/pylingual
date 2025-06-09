def export_file(frame, path, force=False, parts=1):
    """
    Export a given H2OFrame to a path on the machine this python session is currently connected to.

    :param frame: the Frame to save to disk.
    :param path: the path to the save point on disk.
    :param force: if True, overwrite any preexisting file with the same path
    :param parts: enables export to multiple 'part' files instead of just a single file.
        Convenient for large datasets that take too long to store in a single file.
        Use parts=-1 to instruct H2O to determine the optimal number of part files or
        specify your desired maximum number of part files. Path needs to be a directory
        when exporting to multiple files, also that directory must be empty.
        Default is ``parts = 1``, which is to export to a single file.
    """
    assert_is_type(frame, H2OFrame)
    assert_is_type(path, str)
    assert_is_type(force, bool)
    assert_is_type(parts, int)
    H2OJob(api('POST /3/Frames/%s/export' % frame.frame_id, data={'path': path, 'num_parts': parts, 'force': force}), 'Export File').poll()