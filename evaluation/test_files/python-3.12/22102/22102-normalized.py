def stop(self):
    """Stop collecting trace information."""
    assert self._collectors
    assert self._collectors[-1] is self
    self.pause()
    self.tracers = []
    self._collectors.pop()
    if self._collectors:
        self._collectors[-1].resume()