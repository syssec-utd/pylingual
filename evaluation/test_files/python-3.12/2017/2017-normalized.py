def name(self, src=None):
    """Return string representing the name of this type."""
    return ' & '.join((_get_type_name(tt, src) for tt in self._types))