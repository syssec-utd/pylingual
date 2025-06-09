def select_down(self):
    """move cursor down"""
    (r, c) = self._index
    self._select_index(r + 1, c)