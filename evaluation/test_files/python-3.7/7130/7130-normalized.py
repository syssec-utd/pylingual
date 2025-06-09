def write(self, output_stream, kmip_version=enums.KMIPVersion.KMIP_1_0):
    """
        Write the data encoding the Credential struct to a stream.

        Args:
            output_stream (stream): A data stream in which to encode object
                data, supporting a write method; usually a BytearrayStream
                object.
            kmip_version (KMIPVersion): An enumeration defining the KMIP
                version with which the object will be encoded. Optional,
                defaults to KMIP 1.0.

        Raises:
            ValueError: Raised if either the credential type or value are not
                defined.
        """
    local_stream = BytearrayStream()
    if self._credential_type:
        self._credential_type.write(local_stream, kmip_version=kmip_version)
    else:
        raise ValueError('Credential struct missing the credential type.')
    if self._credential_value:
        self._credential_value.write(local_stream, kmip_version=kmip_version)
    else:
        raise ValueError('Credential struct missing the credential value.')
    self.length = local_stream.length()
    super(Credential, self).write(output_stream, kmip_version=kmip_version)
    output_stream.write(local_stream.buffer)