def call_handlers(self, msg):
    """ Reimplemented to emit signals instead of making callbacks.
        """
    self.message_received.emit(msg)
    msg_type = msg['header']['msg_type']
    if msg_type == 'input_request':
        self.input_requested.emit(msg)