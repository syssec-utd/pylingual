def get(self, uid=None, key_wrapping_specification=None):
    """
        Get a managed object from a KMIP appliance.

        Args:
            uid (string): The unique ID of the managed object to retrieve.
            key_wrapping_specification (dict): A dictionary containing various
                settings to be used when wrapping the key during retrieval.
                See Note below. Optional, defaults to None.

        Returns:
            ManagedObject: The retrieved managed object object.

        Raises:
            ClientConnectionNotOpen: if the client connection is unusable
            KmipOperationFailure: if the operation result is a failure
            TypeError: if the input argument is invalid

        Notes:
            The derivation_parameters argument is a dictionary that can
            contain the following key/value pairs:

            Key                             | Value
            --------------------------------|---------------------------------
            'wrapping_method'               | A WrappingMethod enumeration
                                            | that specifies how the object
                                            | should be wrapped.
            'encryption_key_information'    | A dictionary containing the ID
                                            | of the wrapping key and
                                            | associated cryptographic
                                            | parameters.
            'mac_signature_key_information' | A dictionary containing the ID
                                            | of the wrapping key and
                                            | associated cryptographic
                                            | parameters.
            'attribute_names'               | A list of strings representing
                                            | the names of attributes that
                                            | should be included with the
                                            | wrapped object.
            'encoding_option'               | An EncodingOption enumeration
                                            | that specifies the encoding of
                                            | the object before it is wrapped.
        """
    if uid is not None:
        if not isinstance(uid, six.string_types):
            raise TypeError('uid must be a string')
    if key_wrapping_specification is not None:
        if not isinstance(key_wrapping_specification, dict):
            raise TypeError('Key wrapping specification must be a dictionary.')
    spec = self._build_key_wrapping_specification(key_wrapping_specification)
    result = self.proxy.get(uid, key_wrapping_specification=spec)
    status = result.result_status.value
    if status == enums.ResultStatus.SUCCESS:
        managed_object = self.object_factory.convert(result.secret)
        return managed_object
    else:
        reason = result.result_reason.value
        message = result.result_message.value
        raise exceptions.KmipOperationFailure(status, reason, message)