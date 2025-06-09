def write(self, output_buffer, kmip_version=enums.KMIPVersion.KMIP_1_0):
    """
        Write the data encoding the GetAttributeList response payload to a
        stream.

        Args:
            output_buffer (stream): A data stream in which to encode object
                data, supporting a write method; usually a BytearrayStream
                object.
            kmip_version (KMIPVersion): An enumeration defining the KMIP
                version with which the object will be encoded. Optional,
                defaults to KMIP 1.0.

        Raises:
            InvalidField: Raised if the unique identifier or attribute name
                are not defined.
        """
    local_buffer = utils.BytearrayStream()
    if self._unique_identifier:
        self._unique_identifier.write(local_buffer, kmip_version=kmip_version)
    else:
        raise exceptions.InvalidField('The GetAttributeList response payload is missing the unique identifier field.')
    if self._attribute_names:
        if kmip_version < enums.KMIPVersion.KMIP_2_0:
            for attribute_name in self._attribute_names:
                attribute_name.write(local_buffer, kmip_version=kmip_version)
        else:
            for attribute_name in self._attribute_names:
                t = enums.convert_attribute_name_to_tag(attribute_name.value)
                e = primitives.Enumeration(enums.Tags, value=t, tag=enums.Tags.ATTRIBUTE_REFERENCE)
                e.write(local_buffer, kmip_version=kmip_version)
    else:
        raise exceptions.InvalidField('The GetAttributeList response payload is missing the attribute names field.')
    self.length = local_buffer.length()
    super(GetAttributeListResponsePayload, self).write(output_buffer, kmip_version=kmip_version)
    output_buffer.write(local_buffer.buffer)