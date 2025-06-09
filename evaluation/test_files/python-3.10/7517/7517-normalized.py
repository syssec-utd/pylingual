def addSourceAddr(self, addr):
    """None means 'system default'"""
    try:
        self._multiInSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self._makeMreq(addr))
    except socket.error:
        pass
    sock = self._createMulticastOutSocket(addr, self._observer.ttl)
    self._multiOutUniInSockets[addr] = sock
    self._poll.register(sock, select.POLLIN)