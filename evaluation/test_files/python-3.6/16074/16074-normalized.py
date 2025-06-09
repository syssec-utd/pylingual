def propagate_exceptions(self):
    """Returns the value of the `PROPAGATE_EXCEPTIONS` configuration
        value in case it's set, otherwise a sensible default is returned.

        .. versionadded:: 0.7
        """
    rv = self.config['PROPAGATE_EXCEPTIONS']
    if rv is not None:
        return rv
    return self.testing or self.debug