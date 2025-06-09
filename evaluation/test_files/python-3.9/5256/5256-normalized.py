def credits(self, **kwargs):
    """
        Get the cast & crew credits for a TV season by season number.

        Returns:
            A dict respresentation of the JSON returned from the API.
        """
    path = self._get_series_id_season_number_path('credits')
    response = self._GET(path, kwargs)
    self._set_attrs_to_values(response)
    return response