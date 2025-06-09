def _set_ocsp_callback(self, helper, data):
    """
        This internal helper does the common work for
        ``set_ocsp_server_callback`` and ``set_ocsp_client_callback``, which is
        almost all of it.
        """
    self._ocsp_helper = helper
    self._ocsp_callback = helper.callback
    if data is None:
        self._ocsp_data = _ffi.NULL
    else:
        self._ocsp_data = _ffi.new_handle(data)
    rc = _lib.SSL_CTX_set_tlsext_status_cb(self._context, self._ocsp_callback)
    _openssl_assert(rc == 1)
    rc = _lib.SSL_CTX_set_tlsext_status_arg(self._context, self._ocsp_data)
    _openssl_assert(rc == 1)