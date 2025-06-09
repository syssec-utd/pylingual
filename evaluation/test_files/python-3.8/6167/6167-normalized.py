def path_string(s):
    """
    Convert a Python string to a :py:class:`bytes` string identifying the same
    path and which can be passed into an OpenSSL API accepting a filename.

    :param s: An instance of :py:class:`bytes` or :py:class:`unicode`.

    :return: An instance of :py:class:`bytes`.
    """
    if isinstance(s, binary_type):
        return s
    elif isinstance(s, text_type):
        return s.encode(sys.getfilesystemencoding())
    else:
        raise TypeError('Path must be represented as bytes or unicode string')