def f_get_default(self, name, default=None, fast_access=True, with_links=True, shortcuts=True, max_depth=None, auto_load=False):
    """ Similar to `f_get`, but returns the default value if `name` is not found in the
        trajectory.

        This function uses the `f_get` method and will return the default value
        in case `f_get` raises an AttributeError or a DataNotInStorageError.
        Other errors are not handled.

        In contrast to `f_get`, fast access is True by default.

        """
    try:
        return self.f_get(name, fast_access=fast_access, shortcuts=shortcuts, max_depth=max_depth, auto_load=auto_load, with_links=with_links)
    except (AttributeError, pex.DataNotInStorageError):
        return default