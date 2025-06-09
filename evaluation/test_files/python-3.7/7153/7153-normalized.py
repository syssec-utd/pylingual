def read(self, input_buffer, kmip_version=enums.KMIPVersion.KMIP_1_3):
    """
        Read the data encoding the CapabilityInformation structure and decode
        it into its constituent parts.

        Args:
            input_buffer (stream): A data stream containing encoded object
                data, supporting a read method; usually a BytearrayStream
                object.
            kmip_version (KMIPVersion): An enumeration defining the KMIP
                version with which the object will be decoded. Optional,
                defaults to KMIP 2.0.

        Raises:
            VersionNotSupported: Raised when a KMIP version is provided that
                does not support the CapabilityInformation structure.
        """
    if kmip_version < enums.KMIPVersion.KMIP_1_3:
        raise exceptions.VersionNotSupported('KMIP {} does not support the CapabilityInformation object.'.format(kmip_version.value))
    super(CapabilityInformation, self).read(input_buffer, kmip_version=kmip_version)
    local_buffer = utils.BytearrayStream(input_buffer.read(self.length))
    if self.is_tag_next(enums.Tags.STREAMING_CAPABILITY, local_buffer):
        streaming_capability = primitives.Boolean(tag=enums.Tags.STREAMING_CAPABILITY)
        streaming_capability.read(local_buffer, kmip_version=kmip_version)
        self._streaming_capability = streaming_capability
    if self.is_tag_next(enums.Tags.ASYNCHRONOUS_CAPABILITY, local_buffer):
        asynchronous_capability = primitives.Boolean(tag=enums.Tags.ASYNCHRONOUS_CAPABILITY)
        asynchronous_capability.read(local_buffer, kmip_version=kmip_version)
        self._asynchronous_capability = asynchronous_capability
    if self.is_tag_next(enums.Tags.ATTESTATION_CAPABILITY, local_buffer):
        attestation_capability = primitives.Boolean(tag=enums.Tags.ATTESTATION_CAPABILITY)
        attestation_capability.read(local_buffer, kmip_version=kmip_version)
        self._attestation_capability = attestation_capability
    if kmip_version >= enums.KMIPVersion.KMIP_1_4:
        if self.is_tag_next(enums.Tags.BATCH_UNDO_CAPABILITY, local_buffer):
            batch_undo_capability = primitives.Boolean(tag=enums.Tags.BATCH_UNDO_CAPABILITY)
            batch_undo_capability.read(local_buffer, kmip_version=kmip_version)
            self._batch_continue_capability = batch_undo_capability
        if self.is_tag_next(enums.Tags.BATCH_CONTINUE_CAPABILITY, local_buffer):
            batch_continue_capability = primitives.Boolean(tag=enums.Tags.BATCH_CONTINUE_CAPABILITY)
            batch_continue_capability.read(local_buffer, kmip_version=kmip_version)
            self._batch_continue_capability = batch_continue_capability
    if self.is_tag_next(enums.Tags.UNWRAP_MODE, local_buffer):
        unwrap_mode = primitives.Enumeration(enums.UnwrapMode, tag=enums.Tags.UNWRAP_MODE)
        unwrap_mode.read(local_buffer, kmip_version=kmip_version)
        self._unwrap_mode = unwrap_mode
    if self.is_tag_next(enums.Tags.DESTROY_ACTION, local_buffer):
        destroy_action = primitives.Enumeration(enums.DestroyAction, tag=enums.Tags.DESTROY_ACTION)
        destroy_action.read(local_buffer, kmip_version=kmip_version)
        self._destroy_action = destroy_action
    if self.is_tag_next(enums.Tags.SHREDDING_ALGORITHM, local_buffer):
        shredding_algorithm = primitives.Enumeration(enums.ShreddingAlgorithm, tag=enums.Tags.SHREDDING_ALGORITHM)
        shredding_algorithm.read(local_buffer, kmip_version=kmip_version)
        self._shredding_algorithm = shredding_algorithm
    if self.is_tag_next(enums.Tags.RNG_MODE, local_buffer):
        rng_mode = primitives.Enumeration(enums.RNGMode, tag=enums.Tags.RNG_MODE)
        rng_mode.read(local_buffer, kmip_version=kmip_version)
        self._rng_mode = rng_mode
    self.is_oversized(local_buffer)