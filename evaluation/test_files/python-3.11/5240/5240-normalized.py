def info(self, **kwargs):
    """
        Get the basic information for an account.

        Call this method first, before calling other Account methods.

        Returns:
            A dict respresentation of the JSON returned from the API.
        """
    path = self._get_path('info')
    kwargs.update({'session_id': self.session_id})
    response = self._GET(path, kwargs)
    self.id = response['id']
    self._set_attrs_to_values(response)
    return response