def is_modified(self):
    """
        Determines whether this record set has been modified since the
        last retrieval or save.

        :rtype: bool
        :returns: ``True` if the record set has been modified,
            and ``False`` if not.
        """
    for key, val in self._initial_vals.items():
        if getattr(self, key) != val:
            return True
    return False