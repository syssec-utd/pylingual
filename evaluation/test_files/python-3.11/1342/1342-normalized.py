def gen_new_seed(seed, salt):
    """Generate a new seed, from the given seed and salt."""
    if seed is None:
        return None
    string = (str(seed) + salt).encode('utf-8')
    return int(hashlib.md5(string).hexdigest()[:8], 16) & 2147483647