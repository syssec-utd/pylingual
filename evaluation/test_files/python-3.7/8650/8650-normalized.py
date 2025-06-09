def clear(self):
    """Remove all items."""
    self._fwdm.clear()
    self._invm.clear()
    self._sntl.nxt = self._sntl.prv = self._sntl