def method(self, method):
    """
        Defines the HTTP method to match.
        Use ``*`` to match any method.

        Arguments:
            method (str): method value to match. E.g: ``GET``.

        Returns:
            self: current Mock instance.
        """
    self._request.method = method
    self.add_matcher(matcher('MethodMatcher', method))