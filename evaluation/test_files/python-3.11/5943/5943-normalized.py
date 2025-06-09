def save_access_token(self, token, request):
    """Save access token to database.

        A tokensetter is required, which accepts a token and request
        parameters::

            def tokensetter(token, request):
                access_token = Token(
                    client=request.client,
                    user=request.user,
                    token=token['oauth_token'],
                    secret=token['oauth_token_secret'],
                    realms=token['oauth_authorized_realms'],
                )
                return access_token.save()
        """
    log.debug('Save access token %r', token)
    self._tokensetter(token, request)