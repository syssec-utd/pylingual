def acquire(self) -> AcquireChannel:
    """Return the primary acquire channel of this qubit."""
    if self._acquires:
        return self._acquires[0]
    else:
        raise PulseError('No acquire channels in q[%d]' % self._index)