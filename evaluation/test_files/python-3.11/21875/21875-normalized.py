def stop_hb(self):
    """Stop the heartbeating and cancel all related callbacks."""
    if self._beating:
        self._beating = False
        self._hb_periodic_callback.stop()
        if not self.hb_stream.closed():
            self.hb_stream.on_recv(None)