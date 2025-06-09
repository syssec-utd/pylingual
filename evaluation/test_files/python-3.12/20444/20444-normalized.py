def _run_cached_cell_magic(self, magic_name, line):
    """Special method to call a cell magic with the data stored in self.
        """
    cell = self._current_cell_magic_body
    self._current_cell_magic_body = None
    return self.run_cell_magic(magic_name, line, cell)