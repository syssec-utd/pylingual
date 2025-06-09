def is_hash256(s):
    """ Returns True if the considered string is a valid SHA256 hash. """
    if not s or not isinstance(s, str):
        return False
    return re.match('^[0-9A-F]{64}$', s.strip(), re.IGNORECASE)