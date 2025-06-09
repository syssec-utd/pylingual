def release(self, tag, acquire_token):
    """Release the semaphore

        :param tag: A tag identifying what is releasing the semaphore
        :param acquire_token:  The token returned from when the semaphore was
            acquired. Note that this is not really needed to directly use this
            class but is needed for API compatibility with the
            SlidingWindowSemaphore implementation.
        """
    logger.debug('Releasing acquire %s/%s' % (tag, acquire_token))
    self._semaphore.release()