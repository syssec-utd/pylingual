def open_stream(self, bits, channels, rate=None, chunksize=1024, output=True):
    if rate is None:
        rate = int(self.info['defaultSampleRate'])
    is_supported_fmt = self.supports_format(bits, channels, rate, output=output)
    if not is_supported_fmt:
        msg_fmt = ("PyAudioDevice {index} ({name}) doesn't support " + '%s format (Int{bits}, {channels}-channel at' + ' {rate} Hz)') % ('output' if output else 'input')
        msg = msg_fmt.format(index=self.index, name=self.name, bits=bits, channels=channels, rate=rate)
        self._logger.critical(msg)
        raise plugin.audioengine.UnsupportedFormat(msg)
    direction = 'output' if output else 'input'
    stream_kwargs = {'format': bits_to_samplefmt(bits), 'channels': channels, 'rate': rate, 'output': output, 'input': not output, '%s_device_index' % direction: self._index, 'frames_per_buffer': chunksize if output else chunksize * 8}
    stream = self._engine._pyaudio.open(**stream_kwargs)
    '\n        self._logger.debug("%s stream opened on device \'%s\' (%d Hz, %d " +\n                           "channel, %d bit)", "output" if output else "input",\n                           self.slug, rate, channels, bits)\n        '
    try:
        yield stream
    finally:
        stream.close()
        '\n            self._logger.debug("%s stream closed on device \'%s\'",\n                               "output" if output else "input", self.slug)\n            '