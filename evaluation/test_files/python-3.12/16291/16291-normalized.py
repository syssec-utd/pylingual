def dumps(self, obj, salt=None, header_fields=None):
    """Like :meth:`~Serializer.dumps` but creates a JSON Web Signature.  It
        also allows for specifying additional fields to be included in the JWS
        Header.
        """
    header = self.make_header(header_fields)
    signer = self.make_signer(salt, self.algorithm)
    return signer.sign(self.dump_payload(header, obj))