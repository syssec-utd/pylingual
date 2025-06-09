def _locate(path):
    """Search for a relative path and turn it into an absolute path.
    This is handy when hunting for data files to be passed into h2o and used by import file.
    Note: This function is for unit testing purposes only.

    Parameters
    ----------
    path : str
      Path to search for

    :return: Absolute path if it is found.  None otherwise.
    """
    tmp_dir = os.path.realpath(os.getcwd())
    possible_result = os.path.join(tmp_dir, path)
    while True:
        if os.path.exists(possible_result):
            return possible_result
        next_tmp_dir = os.path.dirname(tmp_dir)
        if next_tmp_dir == tmp_dir:
            raise ValueError('File not found: ' + path)
        tmp_dir = next_tmp_dir
        possible_result = os.path.join(tmp_dir, path)