def info(self, **kwargs):
    """
        Get the basic movie information for a specific movie id.

        Args:
            language: (optional) ISO 639-1 code.
            append_to_response: (optional) Comma separated, any movie method.

        Returns:
            A dict representation of the JSON returned from the API.
        """
    path = self._get_id_path('info')
    response = self._GET(path, kwargs)
    self._set_attrs_to_values(response)
    return response