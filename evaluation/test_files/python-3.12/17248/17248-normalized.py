def async_callback(self, callback, *args, **kwargs):
    """Obsolete - catches exceptions from the wrapped function.

        This function is unnecessary since Tornado 1.1.
        """
    if callback is None:
        return None
    if args or kwargs:
        callback = functools.partial(callback, *args, **kwargs)
    return callback