def dispatch_query(self, msg):
    """Route registration requests and queries from clients."""
    try:
        (idents, msg) = self.session.feed_identities(msg)
    except ValueError:
        idents = []
    if not idents:
        self.log.error('Bad Query Message: %r', msg)
        return
    client_id = idents[0]
    try:
        msg = self.session.unserialize(msg, content=True)
    except Exception:
        content = error.wrap_exception()
        self.log.error('Bad Query Message: %r', msg, exc_info=True)
        self.session.send(self.query, 'hub_error', ident=client_id, content=content)
        return
    msg_type = msg['header']['msg_type']
    self.log.info('client::client %r requested %r', client_id, msg_type)
    handler = self.query_handlers.get(msg_type, None)
    try:
        assert handler is not None, 'Bad Message Type: %r' % msg_type
    except:
        content = error.wrap_exception()
        self.log.error('Bad Message Type: %r', msg_type, exc_info=True)
        self.session.send(self.query, 'hub_error', ident=client_id, content=content)
        return
    else:
        handler(idents, msg)