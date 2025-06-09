def resolve(self, method, path):
    """Resolve a request to a route handler.

        Arguments:
          method (str): HTTP method, e.g. GET, POST, etc. (type: str)
          path (str): Request path

        Returns:
          tuple or None: A tuple of three items:

            1. Route handler (callable)
            2. Positional arguments (list)
            3. Keyword arguments (dict)

          ``None`` if no route matches the request.
        """
    if method in self._literal and path in self._literal[method]:
        return (self._literal[method][path], [], {})
    else:
        return self._resolve_non_literal_route(method, path)