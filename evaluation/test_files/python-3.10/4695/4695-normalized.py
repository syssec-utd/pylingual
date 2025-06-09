def _ensure_wrappability(fn):
    """Make sure `fn` can be wrapped cleanly by functools.wraps."""
    if isinstance(fn, (type(object.__init__), type(object.__call__))):
        wrappable_fn = lambda *args, **kwargs: fn(*args, **kwargs)
        wrappable_fn.__name__ = fn.__name__
        wrappable_fn.__doc__ = fn.__doc__
        wrappable_fn.__module__ = ''
        wrappable_fn.__wrapped__ = fn
        return wrappable_fn
    return fn