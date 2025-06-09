def set_version(self, version):
    """
        Set the version number of the certificate. Note that the
        version value is zero-based, eg. a value of 0 is V1.

        :param version: The version number of the certificate.
        :type version: :py:class:`int`

        :return: ``None``
        """
    if not isinstance(version, int):
        raise TypeError('version must be an integer')
    _lib.X509_set_version(self._x509, version)