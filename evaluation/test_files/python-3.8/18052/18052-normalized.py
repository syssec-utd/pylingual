def process(self):
    """ Do connection-based processing (I/O and timers) """
    readfd = []
    writefd = []
    if self.connection.needs_input > 0:
        readfd = [self.socket]
    if self.connection.has_output > 0:
        writefd = [self.socket]
    timeout = None
    deadline = self.connection.next_tick
    if deadline:
        now = time.time()
        timeout = 0 if deadline <= now else deadline - now
    LOG.debug('select() start (t=%s)', str(timeout))
    (readable, writable, ignore) = select.select(readfd, writefd, [], timeout)
    LOG.debug('select() returned')
    if readable:
        try:
            pyngus.read_socket_input(self.connection, self.socket)
        except Exception as e:
            LOG.error('Exception on socket read: %s', str(e))
            self.connection.close_input()
            self.connection.close()
    self.connection.process(time.time())
    if writable:
        try:
            pyngus.write_socket_output(self.connection, self.socket)
        except Exception as e:
            LOG.error('Exception on socket write: %s', str(e))
            self.connection.close_output()
            self.connection.close()