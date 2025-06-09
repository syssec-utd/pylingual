def flush(self):
    """
        Ensure all logging output has been flushed
        """
    if len(self._buffer) > 0:
        self.logger.log(self.level, self._buffer)
        self._buffer = str()