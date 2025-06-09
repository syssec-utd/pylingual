def json_clean(obj):
    """Clean an object to ensure it's safe to encode in JSON.
    
    Atomic, immutable objects are returned unmodified.  Sets and tuples are
    converted to lists, lists are copied and dicts are also copied.

    Note: dicts whose keys could cause collisions upon encoding (such as a dict
    with both the number 1 and the string '1' as keys) will cause a ValueError
    to be raised.

    Parameters
    ----------
    obj : any python object

    Returns
    -------
    out : object
    
      A version of the input which will not cause an encoding error when
      encoded as JSON.  Note that this function does not *encode* its inputs,
      it simply sanitizes it so that there will be no encoding errors later.

    Examples
    --------
    >>> json_clean(4)
    4
    >>> json_clean(range(10))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> sorted(json_clean(dict(x=1, y=2)).items())
    [('x', 1), ('y', 2)]
    >>> sorted(json_clean(dict(x=1, y=2, z=[1,2,3])).items())
    [('x', 1), ('y', 2), ('z', [1, 2, 3])]
    >>> json_clean(True)
    True
    """
    atomic_ok = (unicode, int, types.NoneType)
    container_to_list = (tuple, set, types.GeneratorType)
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return repr(obj)
        return obj
    if isinstance(obj, atomic_ok):
        return obj
    if isinstance(obj, bytes):
        return obj.decode(DEFAULT_ENCODING, 'replace')
    if isinstance(obj, container_to_list) or (hasattr(obj, '__iter__') and hasattr(obj, next_attr_name)):
        obj = list(obj)
    if isinstance(obj, list):
        return [json_clean(x) for x in obj]
    if isinstance(obj, dict):
        nkeys = len(obj)
        nkeys_collapsed = len(set(map(str, obj)))
        if nkeys != nkeys_collapsed:
            raise ValueError('dict can not be safely converted to JSON: key collision would lead to dropped values')
        out = {}
        for k, v in obj.iteritems():
            out[str(k)] = json_clean(v)
        return out
    return repr(obj)