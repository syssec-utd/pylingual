def to_openmath(self, obj):
    """ Convert Python object to OpenMath """
    for cl, conv in reversed(self._conv_to_om):
        if cl is None or isinstance(obj, cl):
            try:
                return conv(obj)
            except CannotConvertError:
                continue
    if hasattr(obj, '__openmath__'):
        return obj.__openmath__()
    raise ValueError('Cannot convert %r to OpenMath.' % obj)