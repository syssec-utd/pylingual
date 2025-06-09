def user_config_files():
    """Return path to any existing user config files
    """
    return filter(os.path.exists, map(os.path.expanduser, config_files))