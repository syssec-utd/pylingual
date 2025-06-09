def dump_privatekey(type, pkey, cipher=None, passphrase=None):
    """
    Dump the private key *pkey* into a buffer string encoded with the type
    *type*.  Optionally (if *type* is :const:`FILETYPE_PEM`) encrypting it
    using *cipher* and *passphrase*.

    :param type: The file type (one of :const:`FILETYPE_PEM`,
        :const:`FILETYPE_ASN1`, or :const:`FILETYPE_TEXT`)
    :param PKey pkey: The PKey to dump
    :param cipher: (optional) if encrypted PEM format, the cipher to use
    :param passphrase: (optional) if encrypted PEM format, this can be either
        the passphrase to use, or a callback for providing the passphrase.

    :return: The buffer with the dumped key in
    :rtype: bytes
    """
    bio = _new_mem_buf()
    if not isinstance(pkey, PKey):
        raise TypeError('pkey must be a PKey')
    if cipher is not None:
        if passphrase is None:
            raise TypeError('if a value is given for cipher one must also be given for passphrase')
        cipher_obj = _lib.EVP_get_cipherbyname(_byte_string(cipher))
        if cipher_obj == _ffi.NULL:
            raise ValueError('Invalid cipher name')
    else:
        cipher_obj = _ffi.NULL
    helper = _PassphraseHelper(type, passphrase)
    if type == FILETYPE_PEM:
        result_code = _lib.PEM_write_bio_PrivateKey(bio, pkey._pkey, cipher_obj, _ffi.NULL, 0, helper.callback, helper.callback_args)
        helper.raise_if_problem()
    elif type == FILETYPE_ASN1:
        result_code = _lib.i2d_PrivateKey_bio(bio, pkey._pkey)
    elif type == FILETYPE_TEXT:
        if _lib.EVP_PKEY_id(pkey._pkey) != _lib.EVP_PKEY_RSA:
            raise TypeError('Only RSA keys are supported for FILETYPE_TEXT')
        rsa = _ffi.gc(_lib.EVP_PKEY_get1_RSA(pkey._pkey), _lib.RSA_free)
        result_code = _lib.RSA_print(bio, rsa, 0)
    else:
        raise ValueError('type argument must be FILETYPE_PEM, FILETYPE_ASN1, or FILETYPE_TEXT')
    _openssl_assert(result_code != 0)
    return _bio_to_string(bio)