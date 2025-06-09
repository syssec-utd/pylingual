def data_received(self, data):
    """Add incoming data to buffer."""
    data = data.decode('ascii')
    self.log.debug('received data: %s', data)
    self.telegram_buffer.append(data)
    for telegram in self.telegram_buffer.get_all():
        self.handle_telegram(telegram)