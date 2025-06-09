def _get_data(self):
    """
        Extracts the session data from cookie.
        """
    cookie = self.adapter.cookies.get(self.name)
    return self._deserialize(cookie) if cookie else {}