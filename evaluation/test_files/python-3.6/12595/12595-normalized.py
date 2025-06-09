def run(self):
    """Starts listening to the queue."""
    try:
        while True:
            (msg, args, kwargs) = self._receive_data()
            stop = self._handle_data(msg, args, kwargs)
            if stop:
                break
    finally:
        if self._storage_service.is_open:
            self._close_file()
        self._trajectory_name = ''