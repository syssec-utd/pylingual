def _format(val, valtype, floatfmt, missingval=''):
    """
    Format a value accoding to its type.

    Unicode is supported:

    >>> hrow = ['буква',                 'цифра'] ;         tbl = [['аз', 2], ['буки', 4]] ;         good_result = '\\u0431\\u0443\\u043a\\u0432\\u0430                              \\u0446\\u0438\\u0444\\u0440\\u0430\\n-------                          -------\\n\\u0430\\u0437                                       2\\n\\u0431\\u0443\\u043a\\u0438           4' ;         tabulate(tbl, headers=hrow) == good_result
    True

    """
    if val is None:
        return missingval
    if valtype in [int, _binary_type, _text_type]:
        return '{0}'.format(val)
    elif valtype is float:
        return format(float(val), floatfmt)
    else:
        return '{0}'.format(val)