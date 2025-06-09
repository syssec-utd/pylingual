def write_async(self, psd_data_or_future, time_start, time_stop, samples):
    """Write PSD of one frequncy hop (asynchronously in another thread)"""
    return self._executor.submit(self.write, psd_data_or_future, time_start, time_stop, samples)