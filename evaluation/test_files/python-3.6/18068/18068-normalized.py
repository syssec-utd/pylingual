def request_sender(self, pn_link):
    """Create link from request for a sender."""
    sl = SenderLink(self._connection, pn_link)
    self._links.add(sl)
    return sl