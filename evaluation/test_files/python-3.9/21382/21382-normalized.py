def reads_json(s, **kwargs):
    """Read a JSON notebook from a string and return the NotebookNode object."""
    (nbf, minor, d) = parse_json(s, **kwargs)
    if nbf == 1:
        nb = v1.to_notebook_json(d, **kwargs)
        nb = v3.convert_to_this_nbformat(nb, orig_version=1)
    elif nbf == 2:
        nb = v2.to_notebook_json(d, **kwargs)
        nb = v3.convert_to_this_nbformat(nb, orig_version=2)
    elif nbf == 3:
        nb = v3.to_notebook_json(d, **kwargs)
        nb = v3.convert_to_this_nbformat(nb, orig_version=3, orig_minor=minor)
    else:
        raise NBFormatError('Unsupported JSON nbformat version: %i' % nbf)
    return nb