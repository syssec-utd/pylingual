def _maybeBind(self):
    """
        Bind the server unless it is already bound, this is a read-only node, or the last attempt was too recently.

        :raises TransportNotReadyError if the bind attempt fails
        """
    if self._ready or self._selfIsReadonlyNode or time.time() < self._lastBindAttemptTime + self._syncObj.conf.bindRetryTime:
        return
    self._lastBindAttemptTime = time.time()
    try:
        self._server.bind()
    except Exception as e:
        self._bindAttempts += 1
        if self._syncObj.conf.maxBindRetries and self._bindAttempts >= self._syncObj.conf.maxBindRetries:
            self._bindOverEvent.set()
            raise TransportNotReadyError
    else:
        self._ready = True
        self._bindOverEvent.set()