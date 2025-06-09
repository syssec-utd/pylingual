def set_mode(self, mode):
    """
        Add modes via bitmask. Modes set before are not cleared!  This method
        should be used with the :const:`MODE_*` constants.

        :param mode: The mode to add.
        :return: The new mode bitmask.
        """
    if not isinstance(mode, integer_types):
        raise TypeError('mode must be an integer')
    return _lib.SSL_CTX_set_mode(self._context, mode)