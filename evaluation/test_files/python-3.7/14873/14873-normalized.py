def send(self, message):
    """ Send a message object

            :type message: data.OutgoingMessage
            :param message: The message to send
            :rtype: data.OutgoingMessage
            :returns: The sent message with populated fields
            :raises AssertionError: wrong provider name encountered (returned by the router, or provided to OutgoingMessage)
            :raises MessageSendError: generic errors
            :raises AuthError: provider authentication failed
            :raises LimitsError: sending limits exceeded
            :raises CreditError: not enough money on the account
        """
    provider_name = self._default_provider
    if message.provider is not None:
        assert message.provider in self._providers, 'Unknown provider specified in OutgoingMessage.provideer: {}'.format(provider_name)
        provider = self.get_provider(message.provider)
    else:
        if message.routing_values is not None:
            provider_name = self.router(message, *message.routing_values) or self._default_provider
            assert provider_name in self._providers, 'Routing function returned an unknown provider name: {}'.format(provider_name)
        provider = self.get_provider(provider_name)
    message.provider = provider.name
    message = provider.send(message)
    self.onSend(message)
    return message