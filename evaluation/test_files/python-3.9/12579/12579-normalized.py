def run(self):
    """Runs server"""
    try:
        self._start()
        running = True
        while running:
            msg = ''
            name = ''
            client_id = ''
            request_id = ''
            request = self._socket.recv_string()
            self._logger.log(1, 'Recevied REQ `%s`', request)
            split_msg = request.split(self.DELIMITER)
            if len(split_msg) == 4:
                (msg, name, client_id, request_id) = split_msg
            if msg == self.LOCK:
                response = self._lock(name, client_id, request_id)
            elif msg == self.UNLOCK:
                response = self._unlock(name, client_id, request_id)
            elif msg == self.PING:
                response = self.PONG
            elif msg == self.DONE:
                response = self.CLOSED
                running = False
            else:
                response = self.MSG_ERROR + self.DELIMITER + 'Request `%s` not understood (or wrong number of delimiters)' % request
                self._logger.error(response)
            respond = self._pre_respond_hook(response)
            if respond:
                self._logger.log(1, 'Sending REP `%s` to `%s` (request id `%s`)', response, client_id, request_id)
                self._socket.send_string(response)
        self._close()
    except Exception:
        self._logger.exception('Crashed Lock Server!')
        raise