def get_qual_range(qual_str):
    """ Get range of the Unicode encode range for a given string of characters.

    The encoding is determined from the result of the :py:func:`ord` built-in.

    Parameters
    ----------
    qual_str : str
        Arbitrary string.

    Returns
    -------
    x : tuple
        (Minimum Unicode code, Maximum Unicode code).
    """
    vals = [ord(c) for c in qual_str]
    return (min(vals), max(vals))