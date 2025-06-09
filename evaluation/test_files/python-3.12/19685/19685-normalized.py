def _ping_loop_iteration(self):
    """
        Called every `ping_interval` seconds.
        Invokes `_ping()` remotely for every ongoing call.
        """
    deferredList = []
    for peerid, callid in list(self._local_to_remote):
        if (peerid, callid) not in self._local_to_remote:
            continue
        logger.debug('sending ping')
        d = self._invoke_function(peerid, self._PING, (self._connectionpool.ownid, callid), {})

        def failed(failure):
            if (peerid, callid) in self._local_to_remote:
                d = self._local_to_remote.pop((peerid, callid))
                d.errback(failure)

        def success(value):
            logger.debug('received pong')
            return value
        d.addCallbacks(success, failed)
        deferredList.append(d)
    d = defer.DeferredList(deferredList)

    def done(_):
        self._ping_current_iteration = None
    self._ping_current_iteration = d
    d.addBoth(done)
    return d