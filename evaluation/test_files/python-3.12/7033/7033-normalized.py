def create(cls, hashing_algorithm=HashingAlgorithmEnum.SHA_256, digest_value=b'', key_format_type=KeyFormatTypeEnum.RAW):
    """
        Construct a Digest object from provided digest values.

        Args:
            hashing_algorithm (HashingAlgorithm): An enumeration representing
                the hash algorithm used to compute the digest. Optional,
                defaults to HashingAlgorithm.SHA_256.
            digest_value (byte string): The bytes of the digest hash. Optional,
                defaults to the empty byte string.
            key_format_type (KeyFormatType): An enumeration representing the
                format of the key corresponding to the digest. Optional,
                defaults to KeyFormatType.RAW.

        Returns:
            Digest: The newly created Digest.

        Example:
            >>> x = Digest.create(HashingAlgorithm.MD5, b'\x00',
            ... KeyFormatType.RAW)
            >>> x.hashing_algorithm
            HashingAlgorithm(value=HashingAlgorithm.MD5)
            >>> x.digest_value
            DigestValue(value=bytearray(b'\x00'))
            >>> x.key_format_type
            KeyFormatType(value=KeyFormatType.RAW)
        """
    algorithm = HashingAlgorithm(hashing_algorithm)
    value = DigestValue(bytearray(digest_value))
    format_type = KeyFormatType(key_format_type)
    return Digest(hashing_algorithm=algorithm, digest_value=value, key_format_type=format_type)