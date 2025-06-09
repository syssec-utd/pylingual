def make_signer(self, salt=None):
    """A method that creates a new instance of the signer to be used.
        The default implementation uses the :class:`Signer` baseclass.
        """
    if salt is None:
        salt = self.salt
    return self.signer(self.secret_key, salt=salt, **self.signer_kwargs)