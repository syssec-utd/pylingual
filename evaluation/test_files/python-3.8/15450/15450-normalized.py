def sendEvents(self, events):
    """Send a Tensor Event to Riemann"""
    self.pressure += 1
    self.sendString(self.encodeMessage(events))