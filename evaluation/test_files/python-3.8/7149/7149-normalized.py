def read(self, input_buffer, kmip_version=enums.KMIPVersion.KMIP_1_3):
    """
        Read the data encoding the ProfileInformation structure and decode it
        into its constituent parts.

        Args:
            input_buffer (stream): A data stream containing encoded object
                data, supporting a read method; usually a BytearrayStream
                object.
            kmip_version (KMIPVersion): An enumeration defining the KMIP
                version with which the object will be decoded. Optional,
                defaults to KMIP 2.0.

        Raises:
            InvalidKmipEncoding: Raised if the profile name is missing from
                the encoding.
            VersionNotSupported: Raised when a KMIP version is provided that
                does not support the ProfileInformation structure.
        """
    if kmip_version < enums.KMIPVersion.KMIP_1_3:
        raise exceptions.VersionNotSupported('KMIP {} does not support the ProfileInformation object.'.format(kmip_version.value))
    super(ProfileInformation, self).read(input_buffer, kmip_version=kmip_version)
    local_buffer = utils.BytearrayStream(input_buffer.read(self.length))
    if self.is_tag_next(enums.Tags.PROFILE_NAME, local_buffer):
        profile_name = primitives.Enumeration(enums.ProfileName, tag=enums.Tags.PROFILE_NAME)
        profile_name.read(local_buffer, kmip_version=kmip_version)
        self._profile_name = profile_name
    else:
        raise exceptions.InvalidKmipEncoding('The ProfileInformation encoding is missing the profile name.')
    if self.is_tag_next(enums.Tags.SERVER_URI, local_buffer):
        server_uri = primitives.TextString(tag=enums.Tags.SERVER_URI)
        server_uri.read(local_buffer, kmip_version=kmip_version)
        self._server_uri = server_uri
    if self.is_tag_next(enums.Tags.SERVER_PORT, local_buffer):
        server_port = primitives.Integer(tag=enums.Tags.SERVER_PORT)
        server_port.read(local_buffer, kmip_version=kmip_version)
        self._server_port = server_port
    self.is_oversized(local_buffer)