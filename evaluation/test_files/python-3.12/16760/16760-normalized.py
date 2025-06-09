def stop(self):
    """Stop streaming samples from device and delete samples buffer"""
    if not self.device.is_streaming:
        return
    self.device.stop_stream()
    self._writer.close()
    self._bins = None
    self._repeats = None
    self._base_buffer_size = None
    self._max_buffer_size = None
    self._buffer_repeats = None
    self._buffer = None
    self._tune_delay = None
    self._reset_stream = None
    self._psd = None
    self._writer = None