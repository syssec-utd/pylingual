def load_client_ca(self, cafile):
    """
        Load the trusted certificates that will be sent to the client.  Does
        not actually imply any of the certificates are trusted; that must be
        configured separately.

        :param bytes cafile: The path to a certificates file in PEM format.
        :return: None
        """
    ca_list = _lib.SSL_load_client_CA_file(_text_to_bytes_and_warn('cafile', cafile))
    _openssl_assert(ca_list != _ffi.NULL)
    _lib.SSL_CTX_set_client_CA_list(self._context, ca_list)