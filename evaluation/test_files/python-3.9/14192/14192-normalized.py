def variables(self):
    """A list of Theano variables used in this loss."""
    result = [self._target]
    if self._weights is not None:
        result.append(self._weights)
    return result