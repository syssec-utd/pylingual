def server(self):
    """
        All in one endpoints. This property is created automaticly
        if you have implemented all the getters and setters.
        """
    if hasattr(self, '_validator'):
        return Server(self._validator)
    if hasattr(self, '_clientgetter') and hasattr(self, '_tokengetter') and hasattr(self, '_tokensetter') and hasattr(self, '_noncegetter') and hasattr(self, '_noncesetter') and hasattr(self, '_grantgetter') and hasattr(self, '_grantsetter') and hasattr(self, '_verifiergetter') and hasattr(self, '_verifiersetter'):
        validator = OAuth1RequestValidator(clientgetter=self._clientgetter, tokengetter=self._tokengetter, tokensetter=self._tokensetter, grantgetter=self._grantgetter, grantsetter=self._grantsetter, noncegetter=self._noncegetter, noncesetter=self._noncesetter, verifiergetter=self._verifiergetter, verifiersetter=self._verifiersetter, config=self.app.config)
        self._validator = validator
        server = Server(validator)
        if self.app.testing:
            server._check_signature = lambda *args, **kwargs: True
        return server
    raise RuntimeError('application not bound to required getters and setters')