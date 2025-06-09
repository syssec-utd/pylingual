def _file_lines(fname):
    """Return the contents of a named file as a list of lines.

    This function never raises an IOError exception: if the file can't be
    read, it simply returns an empty list."""
    try:
        outfile = open(fname)
    except IOError:
        return []
    else:
        out = outfile.readlines()
        outfile.close()
        return out