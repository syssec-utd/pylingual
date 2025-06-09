def timing(self, stat, value, tags=None):
    """Measure a timing for statistical distribution."""
    self.client.timing(stat=stat, delta=value)