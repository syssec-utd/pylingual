def refresh(self):
    """Reload frame information from the backend H2O server."""
    self._ex._cache.flush()
    self._frame(fill_cache=True)