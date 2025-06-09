def _assign_auth_values(self, http_auth):
    """Take the http_auth value and split it into the attributes that
        carry the http auth username and password

        :param str|tuple http_auth: The http auth value

        """
    if not http_auth:
        pass
    elif isinstance(http_auth, (tuple, list)):
        (self._auth_user, self._auth_password) = http_auth
    elif isinstance(http_auth, str):
        (self._auth_user, self._auth_password) = http_auth.split(':')
    else:
        raise ValueError('HTTP Auth Credentials should be str or tuple, not %s' % type(http_auth))