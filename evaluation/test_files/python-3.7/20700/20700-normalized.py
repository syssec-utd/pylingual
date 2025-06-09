def popkey(dct, key, default=NotGiven):
    """Return dct[key] and delete dct[key].

    If default is given, return it if dct[key] doesn't exist, otherwise raise
    KeyError.  """
    try:
        val = dct[key]
    except KeyError:
        if default is NotGiven:
            raise
        else:
            return default
    else:
        del dct[key]
        return val