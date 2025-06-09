def discover_modules(directory):
    """
    Attempts to list all of the modules and submodules found within a given
    directory tree. This function searches the top-level of the directory
    tree for potential python modules and returns a list of candidate names.

    **Note:** This function returns a list of strings representing
    discovered module names, not the actual, loaded modules.

    :param directory: the directory to search for modules.
    """
    found = list()
    if os.path.isdir(directory):
        for entry in os.listdir(directory):
            next_dir = os.path.join(directory, entry)
            if os.path.isfile(os.path.join(next_dir, MODULE_INIT_FILE)):
                found.append(entry)
    return found