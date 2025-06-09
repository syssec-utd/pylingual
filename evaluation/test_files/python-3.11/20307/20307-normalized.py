def _status_new(self):
    """Print the status of newly finished jobs.

        Return True if any new jobs are reported.

        This call resets its own state every time, so it only reports jobs
        which have finished since the last time it was called."""
    self._update_status()
    new_comp = self._group_report(self._comp_report, 'Completed')
    new_dead = self._group_report(self._dead_report, 'Dead, call jobs.traceback() for details')
    self._comp_report[:] = []
    self._dead_report[:] = []
    return new_comp or new_dead