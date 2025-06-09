def basic_transform(val):
    """A basic transform for strings and integers."""
    if isinstance(val, int):
        return struct.pack('>i', val)
    else:
        return safe_lower_utf8(val)