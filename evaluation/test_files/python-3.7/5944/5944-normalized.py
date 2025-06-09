def save_request_token(self, token, request):
    """Save request token to database.

        A grantsetter is required, which accepts a token and request
        parameters::

            def grantsetter(token, request):
                grant = Grant(
                    token=token['oauth_token'],
                    secret=token['oauth_token_secret'],
                    client=request.client,
                    redirect_uri=oauth.redirect_uri,
                    realms=request.realms,
                )
                return grant.save()
        """
    log.debug('Save request token %r', token)
    self._grantsetter(token, request)