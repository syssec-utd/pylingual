def short_stack():
    """Return a string summarizing the call stack."""
    stack = inspect.stack()[:0:-1]
    return '\n'.join(['%30s : %s @%d' % (t[3], t[1], t[2]) for t in stack])