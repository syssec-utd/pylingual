def _output_changed(self, msg):
    """0x17   outputs state 0x17   + 16/32 bytes"""
    status = {'outputs': {}}
    output_states = list_set_bits(msg, 32)
    self.violated_outputs = output_states
    _LOGGER.debug('Output states: %s, monitored outputs: %s', output_states, self._monitored_outputs)
    for output in self._monitored_outputs:
        status['outputs'][output] = 1 if output in output_states else 0
    _LOGGER.debug('Returning status: %s', status)
    if self._output_changed_callback:
        self._output_changed_callback(status)
    return status