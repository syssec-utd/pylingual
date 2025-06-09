def _getdef(self, obj, oname=''):
    """Return the definition header for any callable object.

        If any exception is generated, None is returned instead and the
        exception is suppressed."""
    try:
        hdef = oname + inspect.formatargspec(*getargspec(obj))
        return py3compat.unicode_to_str(hdef, 'ascii')
    except:
        return None