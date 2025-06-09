def get_single(group, name, path=None):
    """Find a single entry point.

    Returns an :class:`EntryPoint` object, or raises :exc:`NoSuchEntryPoint`
    if no match is found.
    """
    for config, distro in iter_files_distros(path=path):
        if group in config and name in config[group]:
            epstr = config[group][name]
            with BadEntryPoint.err_to_warnings():
                return EntryPoint.from_string(epstr, name, distro)
    raise NoSuchEntryPoint(group, name)