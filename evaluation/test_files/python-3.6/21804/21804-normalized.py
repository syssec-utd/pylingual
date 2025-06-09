def data(fname):
    """Return the contents of a data file of ours."""
    data_file = open(data_filename(fname))
    try:
        return data_file.read()
    finally:
        data_file.close()