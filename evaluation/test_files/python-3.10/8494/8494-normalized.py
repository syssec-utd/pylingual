def _onDeviceStatus(self, client, userdata, pahoMessage):
    """
        Internal callback for device status messages, parses source device from topic string and
        passes the information on to the registerd device status callback
        """
    try:
        status = Status(pahoMessage)
        self.logger.debug('Received %s action from %s' % (status.action, status.clientId))
        if self.deviceStatusCallback:
            self.deviceStatusCallback(status)
    except InvalidEventException as e:
        self.logger.critical(str(e))