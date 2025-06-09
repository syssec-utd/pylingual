def call_handlers(self, msg):
    """ Reimplemented to emit signals instead of making callbacks.
        """
    self.message_received.emit(msg)
    msg_type = msg['header']['msg_type']
    signal = getattr(self, msg_type + '_received', None)
    if signal:
        signal.emit(msg)
    elif msg_type in ('stdout', 'stderr'):
        self.stream_received.emit(msg)