def log_calls(func):
    """Decorator to log function calls."""

    def wrapper(*args, **kargs):
        callStr = '%s(%s)' % (func.__name__, ', '.join([repr(p) for p in args] + ['%s=%s' % (k, repr(v)) for (k, v) in list(kargs.items())]))
        debug('>> %s', callStr)
        ret = func(*args, **kargs)
        debug('<< %s: %s', callStr, repr(ret))
        return ret
    return wrapper