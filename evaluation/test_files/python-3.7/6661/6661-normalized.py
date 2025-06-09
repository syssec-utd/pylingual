def _process_connect_init(self):
    """
        Process INFO received from the server and CONNECT to the server
        with authentication.  It is also responsible of setting up the
        reading and ping interval tasks from the client.
        """
    self._status = Client.CONNECTING
    connection_completed = self._io_reader.readline()
    info_line = (yield from asyncio.wait_for(connection_completed, self.options['connect_timeout']))
    if INFO_OP not in info_line:
        raise NatsError('nats: empty response from server when expecting INFO message')
    (_, info) = info_line.split(INFO_OP + _SPC_, 1)
    try:
        srv_info = json.loads(info.decode())
    except:
        raise NatsError('nats: info message, json parse error')
    self._process_info(srv_info)
    self._server_info = srv_info
    if 'max_payload' in self._server_info:
        self._max_payload = self._server_info['max_payload']
    if 'tls_required' in self._server_info and self._server_info['tls_required']:
        ssl_context = None
        if 'tls' in self.options:
            ssl_context = self.options.get('tls')
        elif self._current_server.uri.scheme == 'tls':
            ssl_context = ssl.create_default_context()
        else:
            raise NatsError('nats: no ssl context provided')
        transport = self._io_writer.transport
        sock = transport.get_extra_info('socket')
        if not sock:
            raise NatsError('nats: unable to get socket')
        yield from self._io_writer.drain()
        (self._io_reader, self._io_writer) = (yield from asyncio.open_connection(loop=self._loop, limit=DEFAULT_BUFFER_SIZE, sock=sock, ssl=ssl_context, server_hostname=self._current_server.uri.hostname))
    if self.is_reconnecting:
        self._ps.reset()
    connect_cmd = self._connect_command()
    self._io_writer.write(connect_cmd)
    self._io_writer.write(PING_PROTO)
    yield from self._io_writer.drain()
    next_op = (yield from self._io_reader.readline())
    if self.options['verbose'] and OK_OP in next_op:
        next_op = (yield from self._io_reader.readline())
    if ERR_OP in next_op:
        err_line = next_op.decode()
        (_, err_msg) = err_line.split(' ', 1)
        raise NatsError('nats: ' + err_msg.rstrip('\r\n'))
    if PONG_PROTO in next_op:
        self._status = Client.CONNECTED
    self._reading_task = self._loop.create_task(self._read_loop())
    self._pongs = []
    self._pings_outstanding = 0
    self._ping_interval_task = self._loop.create_task(self._ping_interval())
    self._flusher_task = self._loop.create_task(self._flusher())