def unit_client(self):
    """Return a TCPClient with same settings of the batch TCP client"""
    client = TCPClient(self.host, self.port, self.prefix)
    self._configure_client(client)
    return client