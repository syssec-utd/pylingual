def get_serial(self):
    """
        Get the serial number.

        The serial number is formatted as a hexadecimal number encoded in
        ASCII.

        :return: The serial number.
        :rtype: bytes
        """
    bio = _new_mem_buf()
    asn1_int = _lib.X509_REVOKED_get0_serialNumber(self._revoked)
    _openssl_assert(asn1_int != _ffi.NULL)
    result = _lib.i2a_ASN1_INTEGER(bio, asn1_int)
    _openssl_assert(result >= 0)
    return _bio_to_string(bio)