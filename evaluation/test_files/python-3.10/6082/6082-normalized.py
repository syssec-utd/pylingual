def load_certificate(type, buffer):
    """
    Load a certificate (X509) from the string *buffer* encoded with the
    type *type*.

    :param type: The file type (one of FILETYPE_PEM, FILETYPE_ASN1)

    :param bytes buffer: The buffer the certificate is stored in

    :return: The X509 object
    """
    if isinstance(buffer, _text_type):
        buffer = buffer.encode('ascii')
    bio = _new_mem_buf(buffer)
    if type == FILETYPE_PEM:
        x509 = _lib.PEM_read_bio_X509(bio, _ffi.NULL, _ffi.NULL, _ffi.NULL)
    elif type == FILETYPE_ASN1:
        x509 = _lib.d2i_X509_bio(bio, _ffi.NULL)
    else:
        raise ValueError('type argument must be FILETYPE_PEM or FILETYPE_ASN1')
    if x509 == _ffi.NULL:
        _raise_current_error()
    return X509._from_raw_x509_ptr(x509)