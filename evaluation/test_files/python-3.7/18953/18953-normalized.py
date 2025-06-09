def _resolve_non_literal_route(self, method, path):
    """Resolve a request to a wildcard or regex route handler.

        Arguments:
          method (str): HTTP method name, e.g. GET, POST, etc.
          path (str): Request path

        Returns:
          tuple or None: A tuple of three items:

            1. Route handler (callable)
            2. Positional arguments (list)
            3. Keyword arguments (dict)

          ``None`` if no route matches the request.
        """
    for route_dict in (self._wildcard, self._regex):
        if method in route_dict:
            for route in reversed(route_dict[method]):
                callback_data = route.match(path)
                if callback_data is not None:
                    return callback_data
    return None