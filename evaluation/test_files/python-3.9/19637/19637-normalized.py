def receiveData(self, connection, data):
    """
        Receives some data for the given protocol.
        """
    try:
        protocol = self._protocols[connection]
    except KeyError:
        raise NoSuchConnection()
    protocol.dataReceived(data)
    return {}