def _get_data_files(data_specs, existing):
    """Expand data file specs into valid data files metadata.

    Parameters
    ----------
    data_specs: list of tuples
        See [createcmdclass] for description.
    existing: list of tuples
        The existing distribution data_files metadata.

    Returns
    -------
    A valid list of data_files items.
    """
    file_data = defaultdict(list)
    for path, files in existing or []:
        file_data[path] = files
    for path, dname, pattern in data_specs or []:
        dname = dname.replace(os.sep, '/')
        offset = len(dname) + 1
        files = _get_files(pjoin(dname, pattern))
        for fname in files:
            root = os.path.dirname(fname)
            full_path = '/'.join([path, root[offset:]])
            if full_path.endswith('/'):
                full_path = full_path[:-1]
            file_data[full_path].append(fname)
    data_files = []
    for path, files in file_data.items():
        data_files.append((path, files))
    return data_files