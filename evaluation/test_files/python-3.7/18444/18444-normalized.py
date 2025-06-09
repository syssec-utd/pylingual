def step_prev_line(self):
    """Sets cursor as end of previous line."""
    if len(self._eol) > 0:
        self.position = self._eol.pop()