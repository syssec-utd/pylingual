def copy_config_file(self, config_file, path=None, overwrite=False):
    """Copy a default config file into the active profile directory.

        Default configuration files are kept in :mod:`IPython.config.default`.
        This function moves these from that location to the working profile
        directory.
        """
    dst = os.path.join(self.location, config_file)
    if os.path.isfile(dst) and (not overwrite):
        return False
    if path is None:
        path = os.path.join(get_ipython_package_dir(), u'config', u'profile', u'default')
    src = os.path.join(path, config_file)
    shutil.copy(src, dst)
    return True