def recv_sub(self, id_, name, params):
    """DDP sub handler."""
    self.api.sub(id_, name, *params)