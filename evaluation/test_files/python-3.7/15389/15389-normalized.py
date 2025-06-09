def sendEvent(self, source, events):
    """Callback that all event sources call when they have a new event
        or list of events
        """
    if isinstance(events, list):
        self.eventCounter += len(events)
    else:
        self.eventCounter += 1
        events = [events]
    queue = self._aggregateQueue(events)
    if queue:
        if source in self.critical or source in self.warn:
            self.setStates(source, queue)
        self.routeEvent(source, queue)
    queue = []
    self.lastEvents[source] = time.time()