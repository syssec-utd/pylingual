def _on_message(self, ws, message):
    """Handles and passes received data to the appropriate handlers.

        :return:
        """
    self._stop_timers()
    (raw, received_at) = (message, time.time())
    self.log.debug('_on_message(): Received new message %s at %s', raw, received_at)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return
    if isinstance(data, dict):
        self._system_handler(data, received_at)
    elif data[1] == 'hb':
        self._heartbeat_handler()
    else:
        self._data_handler(data, received_at)
    self._start_timers()