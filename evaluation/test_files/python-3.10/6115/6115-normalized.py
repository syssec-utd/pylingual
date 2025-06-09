def get_extensions(self):
    """
        Get X.509 extensions in the certificate signing request.

        :return: The X.509 extensions in this request.
        :rtype: :py:class:`list` of :py:class:`X509Extension` objects.

        .. versionadded:: 0.15
        """
    exts = []
    native_exts_obj = _lib.X509_REQ_get_extensions(self._req)
    for i in range(_lib.sk_X509_EXTENSION_num(native_exts_obj)):
        ext = X509Extension.__new__(X509Extension)
        ext._extension = _lib.sk_X509_EXTENSION_value(native_exts_obj, i)
        exts.append(ext)
    return exts