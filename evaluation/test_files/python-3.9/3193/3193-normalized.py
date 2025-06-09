def set_active_range(self, i1, i2):
    """Sets the active_fraction, set picked row to None, and remove selection.

        TODO: we may be able to keep the selection, if we keep the expression, and also the picked row
        """
    logger.debug('set active range to: %r', (i1, i2))
    self._active_fraction = (i2 - i1) / float(self.length_original())
    self._index_start = i1
    self._index_end = i2
    self.select(None)
    self.set_current_row(None)
    self._length_unfiltered = i2 - i1
    self.signal_active_fraction_changed.emit(self, self._active_fraction)