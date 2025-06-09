def connect(self, request):
    """
        Send a CONNECT control packet.
        """
    state = self.__class__.__name__
    return defer.fail(MQTTStateError('Unexpected connect() operation', state))