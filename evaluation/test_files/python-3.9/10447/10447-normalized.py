def resume_reading(self):
    """Public API: resume transport reading."""
    self._loop.add_reader(self._fileno, self._read_ready)
    self._active = True