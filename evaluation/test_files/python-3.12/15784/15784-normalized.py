def normalize_keys(self, items):
    """Return a config dictionary with normalized keys regardless of
        whether the keys were specified in environment variables or in config
        files"""
    normalized = {}
    for key, val in items:
        key = key.replace('_', '-')
        if not key.startswith('--'):
            key = '--%s' % key
        normalized[key] = val
    return normalized