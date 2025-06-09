def safe_unicode(e):
    """unicode(e) with various fallbacks. Used for exceptions, which may not be
    safe to call unicode() on.
    """
    try:
        return unicode(e)
    except UnicodeError:
        pass
    try:
        return py3compat.str_to_unicode(str(e))
    except UnicodeError:
        pass
    try:
        return py3compat.str_to_unicode(repr(e))
    except UnicodeError:
        pass
    return u'Unrecoverably corrupt evalue'