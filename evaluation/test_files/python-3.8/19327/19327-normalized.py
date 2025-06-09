def job_set_done(self, js):
    """
        Called when a job set has been completed or cancelled. If the job set
        was active, the next incomplete job set is loaded from the job set
        queue and is activated.
        """
    if self._closed:
        return
    if self._active_js != js:
        return
    try:
        while self._active_js.is_done():
            logger.debug('job set done')
            self._active_js = self._js_queue.popleft()
            logger.debug('activated job set')
    except IndexError:
        self._active_js = None
    else:
        self._distribute_jobs()