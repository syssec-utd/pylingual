def get_original_scopes(self, refresh_token, request, *args, **kwargs):
    """Get the list of scopes associated with the refresh token.

        This method is used in the refresh token grant flow.  We return
        the scope of the token to be refreshed so it can be applied to the
        new access token.
        """
    log.debug('Obtaining scope of refreshed token.')
    tok = self._tokengetter(refresh_token=refresh_token)
    return tok.scopes