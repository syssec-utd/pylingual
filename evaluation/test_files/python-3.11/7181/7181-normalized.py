def read(self, input_stream, kmip_version=enums.KMIPVersion.KMIP_1_0):
    """
        Read the data encoding the ProtocolVersion struct and decode it into
        its constituent parts.

        Args:
            input_stream (stream): A data stream containing encoded object
                data, supporting a read method; usually a BytearrayStream
                object.
            kmip_version (KMIPVersion): An enumeration defining the KMIP
                version with which the object will be decoded. Optional,
                defaults to KMIP 1.0.

        Raises:
            ValueError: Raised if either the major or minor protocol versions
                are missing from the encoding.
        """
    super(ProtocolVersion, self).read(input_stream, kmip_version=kmip_version)
    local_stream = utils.BytearrayStream(input_stream.read(self.length))
    if self.is_tag_next(enums.Tags.PROTOCOL_VERSION_MAJOR, local_stream):
        self._major = primitives.Integer(tag=enums.Tags.PROTOCOL_VERSION_MAJOR)
        self._major.read(local_stream, kmip_version=kmip_version)
    else:
        raise ValueError('Invalid encoding missing the major protocol version number.')
    if self.is_tag_next(enums.Tags.PROTOCOL_VERSION_MINOR, local_stream):
        self._minor = primitives.Integer(tag=enums.Tags.PROTOCOL_VERSION_MINOR)
        self._minor.read(local_stream, kmip_version=kmip_version)
    else:
        raise ValueError('Invalid encoding missing the minor protocol version number.')
    self.is_oversized(local_stream)