def nrows(self):
    """Number of rows in the dataframe (int)."""
    if not self._ex._cache.nrows_valid():
        self._ex._cache.flush()
        self._frame(fill_cache=True)
    return self._ex._cache.nrows