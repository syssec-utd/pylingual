def write(self, output_stream, kmip_version=enums.KMIPVersion.KMIP_1_0):
    """
        Write the data encoding the KeyWrappingSpecification struct to a
        stream.

        Args:
            output_stream (stream): A data stream in which to encode object
                data, supporting a write method; usually a BytearrayStream
                object.
            kmip_version (KMIPVersion): An enumeration defining the KMIP
                version with which the object will be encoded. Optional,
                defaults to KMIP 1.0.
        """
    local_stream = BytearrayStream()
    if self._wrapping_method:
        self._wrapping_method.write(local_stream, kmip_version=kmip_version)
    else:
        raise ValueError('Invalid struct missing the wrapping method attribute.')
    if self._encryption_key_information:
        self._encryption_key_information.write(local_stream, kmip_version=kmip_version)
    if self._mac_signature_key_information:
        self._mac_signature_key_information.write(local_stream, kmip_version=kmip_version)
    if self._attribute_names:
        for unique_identifier in self._attribute_names:
            unique_identifier.write(local_stream, kmip_version=kmip_version)
    if self._encoding_option:
        self._encoding_option.write(local_stream, kmip_version=kmip_version)
    self.length = local_stream.length()
    super(KeyWrappingSpecification, self).write(output_stream, kmip_version=kmip_version)
    output_stream.write(local_stream.buffer)