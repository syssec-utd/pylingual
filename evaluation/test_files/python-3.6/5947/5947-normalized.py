def server(self):
    """
        All in one endpoints. This property is created automaticly
        if you have implemented all the getters and setters.

        However, if you are not satisfied with the getter and setter,
        you can create a validator with :class:`OAuth2RequestValidator`::

            class MyValidator(OAuth2RequestValidator):
                def validate_client_id(self, client_id):
                    # do something
                    return True

        And assign the validator for the provider::

            oauth._validator = MyValidator()
        """
    expires_in = self.app.config.get('OAUTH2_PROVIDER_TOKEN_EXPIRES_IN')
    token_generator = self.app.config.get('OAUTH2_PROVIDER_TOKEN_GENERATOR', None)
    if token_generator and (not callable(token_generator)):
        token_generator = import_string(token_generator)
    refresh_token_generator = self.app.config.get('OAUTH2_PROVIDER_REFRESH_TOKEN_GENERATOR', None)
    if refresh_token_generator and (not callable(refresh_token_generator)):
        refresh_token_generator = import_string(refresh_token_generator)
    if hasattr(self, '_validator'):
        return Server(self._validator, token_expires_in=expires_in, token_generator=token_generator, refresh_token_generator=refresh_token_generator)
    if hasattr(self, '_clientgetter') and hasattr(self, '_tokengetter') and hasattr(self, '_tokensetter') and hasattr(self, '_grantgetter') and hasattr(self, '_grantsetter'):
        usergetter = None
        if hasattr(self, '_usergetter'):
            usergetter = self._usergetter
        validator_class = self._validator_class
        if validator_class is None:
            validator_class = OAuth2RequestValidator
        validator = validator_class(clientgetter=self._clientgetter, tokengetter=self._tokengetter, grantgetter=self._grantgetter, usergetter=usergetter, tokensetter=self._tokensetter, grantsetter=self._grantsetter)
        self._validator = validator
        return Server(validator, token_expires_in=expires_in, token_generator=token_generator, refresh_token_generator=refresh_token_generator)
    raise RuntimeError('application not bound to required getters')