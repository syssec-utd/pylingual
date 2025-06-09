def setup(self, bins, repeats, base_buffer_size=0, max_buffer_size=0, fft_window='hann', fft_overlap=0.5, crop_factor=0, log_scale=True, remove_dc=False, detrend=None, lnb_lo=0, tune_delay=0, reset_stream=False, max_threads=0, max_queue_size=0):
    """Prepare samples buffer and start streaming samples from device"""
    if self.device.is_streaming:
        self.device.stop_stream()
    base_buffer = self.device.start_stream(buffer_size=base_buffer_size)
    self._bins = bins
    self._repeats = repeats
    self._base_buffer_size = len(base_buffer)
    self._max_buffer_size = max_buffer_size
    (self._buffer_repeats, self._buffer) = self.create_buffer(bins, repeats, self._base_buffer_size, self._max_buffer_size)
    self._tune_delay = tune_delay
    self._reset_stream = reset_stream
    self._psd = psd.PSD(bins, self.device.sample_rate, fft_window=fft_window, fft_overlap=fft_overlap, crop_factor=crop_factor, log_scale=log_scale, remove_dc=remove_dc, detrend=detrend, lnb_lo=lnb_lo, max_threads=max_threads, max_queue_size=max_queue_size)
    self._writer = writer.formats[self._output_format](self._output)