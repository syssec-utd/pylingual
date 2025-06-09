def digest(self, digest_name):
    """
        Return the digest of the X509 object.

        :param digest_name: The name of the digest algorithm to use.
        :type digest_name: :py:class:`bytes`

        :return: The digest of the object, formatted as
            :py:const:`b":"`-delimited hex pairs.
        :rtype: :py:class:`bytes`
        """
    digest = _lib.EVP_get_digestbyname(_byte_string(digest_name))
    if digest == _ffi.NULL:
        raise ValueError('No such digest method')
    result_buffer = _ffi.new('unsigned char[]', _lib.EVP_MAX_MD_SIZE)
    result_length = _ffi.new('unsigned int[]', 1)
    result_length[0] = len(result_buffer)
    digest_result = _lib.X509_digest(self._x509, digest, result_buffer, result_length)
    _openssl_assert(digest_result == 1)
    return b':'.join([b16encode(ch).upper() for ch in _ffi.buffer(result_buffer, result_length[0])])