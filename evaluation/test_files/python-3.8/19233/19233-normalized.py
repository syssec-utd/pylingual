def driver(self):
    """Returns the underlying ImageDriver instance."""
    if self._driver is None:
        self._driver = ImageDriver(self.ds.GetDriver())
    return self._driver