def connect(self, south_peer=None, west_peer=None):
    """connect to peers.  `peers` will be a 3-tuples, of the form:
        (location, north_addr, east_addr)
        as produced by
        """
    if south_peer is not None:
        (location, url, _) = south_peer
        self.south.connect(disambiguate_url(url, location))
    if west_peer is not None:
        (location, _, url) = west_peer
        self.west.connect(disambiguate_url(url, location))