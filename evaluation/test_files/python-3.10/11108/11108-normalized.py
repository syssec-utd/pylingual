def replace(s, replace):
    """Replace multiple values in a string"""
    for r in replace:
        s = s.replace(*r)
    return s