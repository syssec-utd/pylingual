def write(self, output_stream, kmip_version=enums.KMIPVersion.KMIP_1_0):
    """
        Write the data encoding the Archive response payload to a stream.

        Args:
            output_stream (stream): A data stream in which to encode object
                data, supporting a write method; usually a BytearrayStream
                object.
            kmip_version (KMIPVersion): An enumeration defining the KMIP
                version with which the object will be decoded. Optional,
                defaults to KMIP 1.0.

        Raises:
            ValueError: Raised if the data attribute is not defined.
        """
    local_stream = utils.BytearrayStream()
    if self._unique_identifier:
        self._unique_identifier.write(local_stream, kmip_version=kmip_version)
    self.length = local_stream.length()
    super(ArchiveResponsePayload, self).write(output_stream, kmip_version=kmip_version)
    output_stream.write(local_stream.buffer)