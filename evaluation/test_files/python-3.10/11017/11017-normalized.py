def receive(self):
    """
        Receive instructions from Guacamole guacd server.
        """
    start = 0
    while True:
        idx = self._buffer.find(INST_TERM.encode(), start)
        if idx != -1:
            line = self._buffer[:idx + 1].decode()
            self._buffer = self._buffer[idx + 1:]
            self.logger.debug('Received instruction: %s' % line)
            return line
        else:
            start = len(self._buffer)
            buf = self.client.recv(BUF_LEN)
            if not buf:
                self.close()
                self.logger.debug('Failed to receive instruction. Closing.')
                return None
            self._buffer.extend(buf)