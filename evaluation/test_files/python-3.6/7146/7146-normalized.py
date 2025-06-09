def write(self, output_buffer, kmip_version=enums.KMIPVersion.KMIP_2_0):
    """
        Write the DefaultsInformation structure encoding to the data stream.

        Args:
            output_buffer (stream): A data stream in which to encode
                Attributes structure data, supporting a write method.
            kmip_version (enum): A KMIPVersion enumeration defining the KMIP
                version with which the object will be encoded. Optional,
                defaults to KMIP 2.0.

        Raises:
            InvalidField: Raised if the object defaults field is not defined.
            VersionNotSupported: Raised when a KMIP version is provided that
                does not support the DefaultsInformation structure.
        """
    if kmip_version < enums.KMIPVersion.KMIP_2_0:
        raise exceptions.VersionNotSupported('KMIP {} does not support the DefaultsInformation object.'.format(kmip_version.value))
    local_buffer = BytearrayStream()
    if self._object_defaults:
        for object_default in self._object_defaults:
            object_default.write(local_buffer, kmip_version=kmip_version)
    else:
        raise exceptions.InvalidField('The DefaultsInformation structure is missing the object defaults field.')
    self.length = local_buffer.length()
    super(DefaultsInformation, self).write(output_buffer, kmip_version=kmip_version)
    output_buffer.write(local_buffer.buffer)