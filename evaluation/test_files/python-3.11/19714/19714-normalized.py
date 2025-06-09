def request_signed_by_signing_keys(keyjar, msreq, iss, lifetime, kid=''):
    """
    A metadata statement signing request with 'signing_keys' signed by one
    of the keys in 'signing_keys'.

    :param keyjar: A KeyJar instance with the private signing key
    :param msreq: Metadata statement signing request. A MetadataStatement 
        instance.
    :param iss: Issuer of the signing request also the owner of the signing 
        keys.
    :return: Signed JWT where the body is the metadata statement
    """
    try:
        jwks_to_keyjar(msreq['signing_keys'], iss)
    except KeyError:
        jwks = keyjar.export_jwks(issuer=iss)
        msreq['signing_keys'] = jwks
    _jwt = JWT(keyjar, iss=iss, lifetime=lifetime)
    return _jwt.pack(owner=iss, kid=kid, payload=msreq.to_dict())