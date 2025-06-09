def step_next_line(self):
    """Sets cursor as beginning of next line."""
    self._eol.append(self.position)
    self._lineno += 1
    self._col_offset = 0