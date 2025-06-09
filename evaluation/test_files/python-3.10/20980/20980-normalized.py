def deprecated(replacement=None):
    """A decorator which can be used to mark functions as deprecated."""

    def outer(fun):
        msg = 'psutil.%s is deprecated' % fun.__name__
        if replacement is not None:
            msg += '; use %s instead' % replacement
        if fun.__doc__ is None:
            fun.__doc__ = msg

        @wraps(fun)
        def inner(*args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            return fun(*args, **kwargs)
        return inner
    return outer