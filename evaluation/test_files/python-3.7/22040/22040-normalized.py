def squash_unicode(obj):
    """coerce unicode back to bytestrings."""
    if isinstance(obj, dict):
        for key in obj.keys():
            obj[key] = squash_unicode(obj[key])
            if isinstance(key, unicode):
                obj[squash_unicode(key)] = obj.pop(key)
    elif isinstance(obj, list):
        for (i, v) in enumerate(obj):
            obj[i] = squash_unicode(v)
    elif isinstance(obj, unicode):
        obj = obj.encode('utf8')
    return obj