def tolist(val):
    """Convert a value that may be a list or a (possibly comma-separated)
    string into a list. The exception: None is returned as None, not [None].

    >>> tolist(["one", "two"])
    ['one', 'two']
    >>> tolist("hello")
    ['hello']
    >>> tolist("separate,values, with, commas,  spaces , are    ,ok")
    ['separate', 'values', 'with', 'commas', 'spaces', 'are', 'ok']
    """
    if val is None:
        return None
    try:
        val.extend([])
        return val
    except AttributeError:
        pass
    try:
        return re.split('\\s*,\\s*', val)
    except TypeError:
        return list(val)