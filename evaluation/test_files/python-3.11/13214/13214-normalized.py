def get_method(self, key: T) -> Optional[Method]:
    """Return the method which would handle this dispatch key or
        None if no method defined for this key and no default."""
    method_cache = self.methods
    return Maybe(method_cache.entry(key, None)).or_else(lambda: method_cache.entry(self._default, None))