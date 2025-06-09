def _session_set(self, key, value):
    """
        Saves a value to session.
        """
    self.session[self._session_key(key)] = value