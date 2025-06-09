def url(self, endpoint=''):
    """
        Get the base URL of the Remote.

        Arguments:
            None
        Returns:
            `str` base URL
        """
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint
    return self.protocol + '://' + self.hostname + endpoint