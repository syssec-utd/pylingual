def walkFlattenFields(sigOrVal, skipPadding=True):
    """
    Walk all simple values in HStruct or HArray
    """
    t = sigOrVal._dtype
    if isinstance(t, Bits):
        yield sigOrVal
    elif isinstance(t, HUnion):
        yield from walkFlattenFields(sigOrVal._val, skipPadding=skipPadding)
    elif isinstance(t, HStruct):
        for f in t.fields:
            isPadding = f.name is None
            if not isPadding or not skipPadding:
                if isPadding:
                    v = f.dtype.fromPy(None)
                else:
                    v = getattr(sigOrVal, f.name)
                yield from walkFlattenFields(v)
    elif isinstance(t, HArray):
        for item in sigOrVal:
            yield from walkFlattenFields(item)
    else:
        raise NotImplementedError(t)