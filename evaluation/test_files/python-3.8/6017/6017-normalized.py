def use_privatekey(self, pkey):
    """
        Load a private key from a PKey object

        :param pkey: The PKey object
        :return: None
        """
    if not isinstance(pkey, PKey):
        raise TypeError('pkey must be a PKey instance')
    use_result = _lib.SSL_CTX_use_PrivateKey(self._context, pkey._pkey)
    if not use_result:
        self._raise_passphrase_exception()