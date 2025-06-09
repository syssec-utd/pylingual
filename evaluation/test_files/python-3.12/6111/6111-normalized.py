def get_pubkey(self):
    """
        Get the public key of the certificate signing request.

        :return: The public key.
        :rtype: :py:class:`PKey`
        """
    pkey = PKey.__new__(PKey)
    pkey._pkey = _lib.X509_REQ_get_pubkey(self._req)
    _openssl_assert(pkey._pkey != _ffi.NULL)
    pkey._pkey = _ffi.gc(pkey._pkey, _lib.EVP_PKEY_free)
    pkey._only_public = True
    return pkey