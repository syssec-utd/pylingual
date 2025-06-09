def guest_session_new(self, **kwargs):
    """
        Generate a guest session id.

        Returns:
            A dict respresentation of the JSON returned from the API.
        """
    path = self._get_path('guest_session_new')
    response = self._GET(path, kwargs)
    self._set_attrs_to_values(response)
    return response