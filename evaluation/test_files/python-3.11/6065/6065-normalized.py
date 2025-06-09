def get_peer_cert_chain(self):
    """
        Retrieve the other side's certificate (if any)

        :return: A list of X509 instances giving the peer's certificate chain,
                 or None if it does not have one.
        """
    cert_stack = _lib.SSL_get_peer_cert_chain(self._ssl)
    if cert_stack == _ffi.NULL:
        return None
    result = []
    for i in range(_lib.sk_X509_num(cert_stack)):
        cert = _lib.X509_dup(_lib.sk_X509_value(cert_stack, i))
        pycert = X509._from_raw_x509_ptr(cert)
        result.append(pycert)
    return result