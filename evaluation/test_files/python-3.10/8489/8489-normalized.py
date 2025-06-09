def subscribeToDeviceStatus(self, typeId='+', deviceId='+'):
    """
        Subscribe to device status messages

        # Parameters
        typeId (string): typeId for the subscription, optional.  Defaults to all device types (MQTT `+` wildcard)
        deviceId (string): deviceId for the subscription, optional.  Defaults to all devices (MQTT `+` wildcard)

        # Returns
        int: If the subscription was successful then the return Message ID (mid) for the subscribe request
            will be returned. The mid value can be used to track the subscribe request by checking against
            the mid argument if you register a subscriptionCallback method.
            If the subscription fails then the return value will be `0`
        """
    if self._config.isQuickstart() and deviceId == '+':
        self.logger.warning('QuickStart applications do not support wildcard subscription to device status')
        return 0
    topic = 'iot-2/type/%s/id/%s/mon' % (typeId, deviceId)
    return self._subscribe(topic, 0)