def get_subject(self):
    """
        Return the subject of this certificate signing request.

        This creates a new :class:`X509Name` that wraps the underlying subject
        name field on the certificate signing request. Modifying it will modify
        the underlying signing request, and will have the effect of modifying
        any other :class:`X509Name` that refers to this subject.

        :return: The subject of this certificate signing request.
        :rtype: :class:`X509Name`
        """
    name = X509Name.__new__(X509Name)
    name._name = _lib.X509_REQ_get_subject_name(self._req)
    _openssl_assert(name._name != _ffi.NULL)
    name._owner = self
    return name