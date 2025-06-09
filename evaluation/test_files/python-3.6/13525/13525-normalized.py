def make_multi_entry(plist, pkg_pyvers, ver_dict):
    """Generate Python interpreter version entries."""
    for pyver in pkg_pyvers:
        pver = pyver[2] + '.' + pyver[3:]
        plist.append('Python {0}: {1}'.format(pver, ops_to_words(ver_dict[pyver])))