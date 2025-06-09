async def receive_deferred_messages(self, sequence_numbers, mode=ReceiveSettleMode.PeekLock):
    """Receive messages that have previously been deferred.

        This operation can only receive deferred messages from the current session.
        When receiving deferred messages from a partitioned entity, all of the supplied
        sequence numbers must be messages from the same partition.

        :param sequence_numbers: A list of the sequence numbers of messages that have been
         deferred.
        :type sequence_numbers: list[int]
        :param mode: The receive mode, default value is PeekLock.
        :type mode: ~azure.servicebus.common.constants.ReceiveSettleMode
        :rtype: list[~azure.servicebus.aio.async_message.DeferredMessage]

        Example:
            .. literalinclude:: ../examples/async_examples/test_examples_async.py
                :start-after: [START receiver_defer_session_messages]
                :end-before: [END receiver_defer_session_messages]
                :language: python
                :dedent: 8
                :caption: Defer messages, then retrieve them by sequence number.

        """
    if not sequence_numbers:
        raise ValueError('At least one sequence number must be specified.')
    await self._can_run()
    try:
        receive_mode = mode.value.value
    except AttributeError:
        receive_mode = int(mode)
    message = {'sequence-numbers': types.AMQPArray([types.AMQPLong(s) for s in sequence_numbers]), 'receiver-settle-mode': types.AMQPuInt(receive_mode), 'session-id': self.session_id}
    handler = functools.partial(mgmt_handlers.deferred_message_op, mode=receive_mode, message_type=DeferredMessage)
    messages = await self._mgmt_request_response(REQUEST_RESPONSE_RECEIVE_BY_SEQUENCE_NUMBER, message, handler)
    for m in messages:
        m._receiver = self
    return messages