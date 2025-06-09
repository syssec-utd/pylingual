def recv(self, socket, mode=zmq.NOBLOCK, content=True, copy=True):
    """Receive and unpack a message.

        Parameters
        ----------
        socket : ZMQStream or Socket
            The socket or stream to use in receiving.

        Returns
        -------
        [idents], msg
            [idents] is a list of idents and msg is a nested message dict of
            same format as self.msg returns.
        """
    if isinstance(socket, ZMQStream):
        socket = socket.socket
    try:
        msg_list = socket.recv_multipart(mode, copy=copy)
    except zmq.ZMQError as e:
        if e.errno == zmq.EAGAIN:
            return (None, None)
        else:
            raise
    idents, msg_list = self.feed_identities(msg_list, copy)
    try:
        return (idents, self.unserialize(msg_list, content=content, copy=copy))
    except Exception as e:
        raise e