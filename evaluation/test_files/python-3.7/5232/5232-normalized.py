def rating(self, **kwargs):
    """
        This method lets users rate a movie. A valid session id or guest
        session id is required.

        Args:
            session_id: see Authentication.
            guest_session_id: see Authentication.
            value: Rating value.

        Returns:
            A dict representation of the JSON returned from the API.
        """
    path = self._get_id_path('rating')
    payload = {'value': kwargs.pop('value', None)}
    response = self._POST(path, kwargs, payload)
    self._set_attrs_to_values(response)
    return response