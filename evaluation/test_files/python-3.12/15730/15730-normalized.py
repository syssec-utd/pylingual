def __on_open(self, ws):
    """Called when the websocket is opened"""
    logging.debug('ConnectorDB: Websocket opened')
    self.reconnect_time /= self.reconnect_time_backoff_multiplier
    self.status = 'connected'
    self.lastpingtime = time.time()
    self.__ensure_ping()
    self.connected_time = time.time()
    self.ws_openlock.release()