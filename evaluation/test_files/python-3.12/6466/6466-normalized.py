def check_standard_dir(module_path):
    """Checks whether path belongs to standard library or installed modules."""
    if 'site-packages' in module_path:
        return True
    for stdlib_path in _STDLIB_PATHS:
        if fnmatch.fnmatchcase(module_path, stdlib_path + '*'):
            return True
    return False