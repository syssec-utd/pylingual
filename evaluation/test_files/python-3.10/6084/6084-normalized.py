def dump_publickey(type, pkey):
    """
    Dump a public key to a buffer.

    :param type: The file type (one of :data:`FILETYPE_PEM` or
        :data:`FILETYPE_ASN1`).
    :param PKey pkey: The public key to dump
    :return: The buffer with the dumped key in it.
    :rtype: bytes
    """
    bio = _new_mem_buf()
    if type == FILETYPE_PEM:
        write_bio = _lib.PEM_write_bio_PUBKEY
    elif type == FILETYPE_ASN1:
        write_bio = _lib.i2d_PUBKEY_bio
    else:
        raise ValueError('type argument must be FILETYPE_PEM or FILETYPE_ASN1')
    result_code = write_bio(bio, pkey._pkey)
    if result_code != 1:
        _raise_current_error()
    return _bio_to_string(bio)