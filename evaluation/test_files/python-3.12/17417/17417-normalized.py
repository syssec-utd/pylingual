def utf8(data):
    """Convert a basestring to a valid UTF-8 str."""
    if isinstance(data, bytes):
        return data.decode('utf-8', 'replace').encode('utf-8')
    elif isinstance(data, text_type):
        return data.encode('utf-8')
    else:
        raise TypeError('only unicode/bytes types can be converted to UTF-8')