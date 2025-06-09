def validate_user(self, username, password, client, request, *args, **kwargs):
    """Ensure the username and password is valid.

        Attach user object on request for later using.
        """
    log.debug('Validating username %r and its password', username)
    if self._usergetter is not None:
        user = self._usergetter(username, password, client, request, *args, **kwargs)
        if user:
            request.user = user
            return True
        return False
    log.debug('Password credential authorization is disabled.')
    return False