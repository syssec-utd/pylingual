def load_next(mod, altmod, name, buf):
    """
    mod, name, buf = load_next(mod, altmod, name, buf)

    altmod is either None or same as mod
    """
    if len(name) == 0:
        return (mod, None, buf)
    dot = name.find('.')
    if dot == 0:
        raise ValueError('Empty module name')
    if dot < 0:
        subname = name
        next = None
    else:
        subname = name[:dot]
        next = name[dot + 1:]
    if buf != '':
        buf += '.'
    buf += subname
    result = import_submodule(mod, subname, buf)
    if result is None and mod != altmod:
        result = import_submodule(altmod, subname, subname)
        if result is not None:
            buf = subname
    if result is None:
        raise ImportError('No module named %.200s' % name)
    return (result, next, buf)