def derive_key(self, object_type, unique_identifiers, derivation_method, derivation_parameters, template_attribute, credential=None):
    """
        Derive a new key or secret data from an existing managed object.

        Args:
            object_type (ObjectType): An ObjectType enumeration specifying
                what type of object to create. Required.
            unique_identifiers (list): A list of strings specifying the unique
                IDs of the existing managed objects to use for key derivation.
                Required.
            derivation_method (DerivationMethod): A DerivationMethod
                enumeration specifying what key derivation method to use.
                Required.
            derivation_parameters (DerivationParameters): A
                DerivationParameters struct containing the settings and
                options to use for key derivation.
            template_attribute (TemplateAttribute): A TemplateAttribute struct
                containing the attributes to set on the newly derived object.
            credential (Credential): A Credential struct containing a set of
                authorization parameters for the operation. Optional, defaults
                to None.

        Returns:
            dict: The results of the derivation operation, containing the
                following key/value pairs:

                Key                  | Value
                ---------------------|-----------------------------------------
                'unique_identifier'  | (string) The unique ID of the newly
                                     | derived object.
                'template_attribute' | (TemplateAttribute) A struct containing
                                     | any attributes set on the newly derived
                                     | object.
                'result_status'      | (ResultStatus) An enumeration indicating
                                     | the status of the operation result.
                'result_reason'      | (ResultReason) An enumeration providing
                                     | context for the result status.
                'result_message'     | (string) A message providing additional
                                     | context for the operation result.
        """
    operation = Operation(OperationEnum.DERIVE_KEY)
    request_payload = payloads.DeriveKeyRequestPayload(object_type=object_type, unique_identifiers=unique_identifiers, derivation_method=derivation_method, derivation_parameters=derivation_parameters, template_attribute=template_attribute)
    batch_item = messages.RequestBatchItem(operation=operation, request_payload=request_payload)
    request = self._build_request_message(credential, [batch_item])
    response = self._send_and_receive_message(request)
    batch_item = response.batch_items[0]
    payload = batch_item.response_payload
    result = {}
    if payload:
        result['unique_identifier'] = payload.unique_identifier
        result['template_attribute'] = payload.template_attribute
    result['result_status'] = batch_item.result_status.value
    try:
        result['result_reason'] = batch_item.result_reason.value
    except Exception:
        result['result_reason'] = batch_item.result_reason
    try:
        result['result_message'] = batch_item.result_message.value
    except Exception:
        result['result_message'] = batch_item.result_message
    return result