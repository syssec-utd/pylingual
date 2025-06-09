def _uniquote(value):
    """
    Convert to unicode, and add quotes if initially a string
    """
    if isinstance(value, six.binary_type):
        try:
            value = value.decode('utf-8')
        except UnicodeDecodeError:
            value = six.text_type(_dequote(repr(value)))
    result = six.text_type(value)
    if isinstance(value, six.text_type):
        result = "'%s'" % result
    return result