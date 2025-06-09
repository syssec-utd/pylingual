def is_valid_filesys(path):
    """Checks if the path is correct and exists, must be abs-> a dir -> and not a file."""
    if os.path.isabs(path) and os.path.isdir(path) and (not os.path.isfile(path)):
        return True
    else:
        raise LocalPortValidationError('Port value %s is not a valid filesystem location' % path)