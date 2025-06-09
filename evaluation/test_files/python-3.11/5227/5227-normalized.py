def upcoming(self, **kwargs):
    """
        Get the list of upcoming movies. This list refreshes every day.
        The maximum number of items this list will include is 100.

        Args:
            page: (optional) Minimum value of 1.  Expected value is an integer.
            language: (optional) ISO 639-1 code.

        Returns:
            A dict representation of the JSON returned from the API.
        """
    path = self._get_path('upcoming')
    response = self._GET(path, kwargs)
    self._set_attrs_to_values(response)
    return response