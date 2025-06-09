def _spin_every(self, interval=1):
    """target func for use in spin_thread"""
    while True:
        if self._stop_spinning.is_set():
            return
        time.sleep(interval)
        self.spin()