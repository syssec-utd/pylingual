def values_search(self, **params):
    """ Method for `Search Values from all Data Streams of a Device <https://m2x.att.com/developer/documentation/v2/device#Search-Values-from-all-Data-Streams-of-a-Device>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
    return self.api.post(self.subpath('/values/search'), data=params)