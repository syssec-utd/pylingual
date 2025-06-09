def fetch_next(self, max_batch_size=None, timeout=None):
    """Receive a batch of messages at once.

        This approach it optimal if you wish to process multiple messages simultaneously. Note that the
        number of messages retrieved in a single batch will be dependent on
        whether `prefetch` was set for the receiver. This call will prioritize returning
        quickly over meeting a specified batch size, and so will return as soon as at least
        one message is received and there is a gap in incoming messages regardless
        of the specified batch size.

        :param max_batch_size: Maximum number of messages in the batch. Actual number
         returned will depend on prefetch size and incoming stream rate.
        :type max_batch_size: int
        :param timeout: The time to wait in seconds for the first message to arrive.
         If no messages arrive, and no timeout is specified, this call will not return
         until the connection is closed. If specified, an no messages arrive within the
         timeout period, an empty list will be returned.
        :rtype: list[~azure.servicebus.common.message.Message]

        Example:
            .. literalinclude:: ../examples/test_examples.py
                :start-after: [START fetch_next_messages]
                :end-before: [END fetch_next_messages]
                :language: python
                :dedent: 4
                :caption: Get the messages in batch from the receiver

        """
    self._can_run()
    wrapped_batch = []
    max_batch_size = max_batch_size or self._handler._prefetch
    try:
        timeout_ms = 1000 * timeout if timeout else 0
        batch = self._handler.receive_message_batch(max_batch_size=max_batch_size, timeout=timeout_ms)
        for received in batch:
            message = self._build_message(received)
            wrapped_batch.append(message)
    except Exception as e:
        self._handle_exception(e)
    return wrapped_batch