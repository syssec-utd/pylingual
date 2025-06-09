def _on_merge(self, other):
    """
        After merging statements update IO, sensitivity and context

        :attention: rank is not updated
        """
    self._inputs.extend(other._inputs)
    self._outputs.extend(other._outputs)
    if self._sensitivity is not None:
        self._sensitivity.extend(other._sensitivity)
    else:
        assert other._sensitivity is None
    if self._enclosed_for is not None:
        self._enclosed_for.update(other._enclosed_for)
    else:
        assert other._enclosed_for is None
    other_was_top = other.parentStm is None
    if other_was_top:
        other._get_rtl_context().statements.remove(other)
        for s in other._inputs:
            s.endpoints.discard(other)
            s.endpoints.append(self)
        for s in other._outputs:
            s.drivers.discard(other)
            s.drivers.append(self)