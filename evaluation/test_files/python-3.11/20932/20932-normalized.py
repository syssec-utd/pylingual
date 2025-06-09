def dispatch_control(self, msg):
    """dispatch control requests"""
    idents, msg = self.session.feed_identities(msg, copy=False)
    try:
        msg = self.session.unserialize(msg, content=True, copy=False)
    except:
        self.log.error('Invalid Control Message', exc_info=True)
        return
    self.log.debug('Control received: %s', msg)
    header = msg['header']
    msg_id = header['msg_id']
    msg_type = header['msg_type']
    handler = self.control_handlers.get(msg_type, None)
    if handler is None:
        self.log.error('UNKNOWN CONTROL MESSAGE TYPE: %r', msg_type)
    else:
        try:
            handler(self.control_stream, idents, msg)
        except Exception:
            self.log.error('Exception in control handler:', exc_info=True)