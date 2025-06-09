def load_verify_locations(self, cafile, capath=None):
    """
        Let SSL know where we can find trusted certificates for the certificate
        chain.  Note that the certificates have to be in PEM format.

        If capath is passed, it must be a directory prepared using the
        ``c_rehash`` tool included with OpenSSL.  Either, but not both, of
        *pemfile* or *capath* may be :data:`None`.

        :param cafile: In which file we can find the certificates (``bytes`` or
            ``unicode``).
        :param capath: In which directory we can find the certificates
            (``bytes`` or ``unicode``).

        :return: None
        """
    if cafile is None:
        cafile = _ffi.NULL
    else:
        cafile = _path_string(cafile)
    if capath is None:
        capath = _ffi.NULL
    else:
        capath = _path_string(capath)
    load_result = _lib.SSL_CTX_load_verify_locations(self._context, cafile, capath)
    if not load_result:
        _raise_current_error()