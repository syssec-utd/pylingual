def digest(self, data, mecha=MechanismSHA1):
    """
        C_DigestInit/C_Digest

        :param data: the data to be digested
        :type data:  (binary) sring or list/tuple of bytes
        :param mecha: the digesting mechanism to be used
          (use `MechanismSHA1` for `CKM_SHA_1`)
        :type mecha: :class:`Mechanism`
        :return: the computed digest
        :rtype: list of bytes

        :note: the returned value is an istance of :class:`ckbytelist`.
          You can easly convert it to a binary string with:
          ``bytes(ckbytelistDigest)``
          or, for Python 2:
          ``''.join(chr(i) for i in ckbytelistDigest)``

        """
    digest = ckbytelist()
    m = mecha.to_native()
    data1 = ckbytelist(data)
    rv = self.lib.C_DigestInit(self.session, m)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)
    rv = self.lib.C_Digest(self.session, data1, digest)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)
    rv = self.lib.C_Digest(self.session, data1, digest)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)
    return digest