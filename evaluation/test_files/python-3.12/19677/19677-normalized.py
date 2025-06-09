def dataReceived(self, data):
    """
        Do not overwrite this method. Instead implement `on_...` methods for the
        registered typenames to handle incomming packets.
        """
    self._unprocessed_data.enqueue(data)
    while True:
        if len(self._unprocessed_data) < self._header.size:
            return
        hdr_data = self._unprocessed_data.peek(self._header.size)
        packet_length, typekey = self._header.unpack(hdr_data)
        total_length = self._header.size + packet_length
        if len(self._unprocessed_data) < total_length:
            return
        self._unprocessed_data.drop(self._header.size)
        packet = self._unprocessed_data.dequeue(packet_length)
        self._start_receive = None
        typename = self._type_register.get(typekey, None)
        if typename is None:
            self.on_unregistered_type(typekey, packet)
        else:
            self.packet_received(typename, packet)