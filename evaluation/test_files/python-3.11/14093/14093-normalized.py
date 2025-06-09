def read_bytes(self, addr, number):
    """Read many bytes from the specified device."""
    assert self._device is not None, 'Bus must be opened before operations are made against it!'
    self._select_device(addr)
    return self._device.read(number)