def connect(self):
    """connect to the server"""
    if self.loop is None:
        self.loop = asyncio.get_event_loop()
    t = asyncio.Task(self.loop.create_connection(self.config['protocol_factory'], self.config['host'], self.config['port'], ssl=self.config['ssl']), loop=self.loop)
    t.add_done_callback(self.connection_made)
    return t