def add_result(self, result):
    """
        Adds the result of a completed job to the result list, then decrements
        the active job count. If the job set is already complete, the result is
        simply discarded instead.
        """
    if self._active_jobs == 0:
        return
    self._results.add(result)
    self._active_jobs -= 1
    if self._active_jobs == 0:
        self._done()