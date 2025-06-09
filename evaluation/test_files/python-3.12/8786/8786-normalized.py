def dump(obj, file, reducers=None, protocol=None):
    """Replacement for pickle.dump() using _LokyPickler."""
    global _LokyPickler
    _LokyPickler(file, reducers=reducers, protocol=protocol).dump(obj)