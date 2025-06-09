def unregister_transformer(self, transformer):
    """Unregister a transformer instance."""
    if transformer in self._transformers:
        self._transformers.remove(transformer)