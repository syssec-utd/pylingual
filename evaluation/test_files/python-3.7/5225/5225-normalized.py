def reviews(self, **kwargs):
    """
        Get the reviews for a particular movie id.

        Args:
            page: (optional) Minimum value of 1.  Expected value is an integer.
            language: (optional) ISO 639-1 code.
            append_to_response: (optional) Comma separated, any movie method.

        Returns:
            A dict representation of the JSON returned from the API.
        """
    path = self._get_id_path('reviews')
    response = self._GET(path, kwargs)
    self._set_attrs_to_values(response)
    return response