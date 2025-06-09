def swap_slot_slot(self, resource_group_name, name, slot, target_slot, preserve_vnet, custom_headers=None, raw=False, polling=True, **operation_config):
    """Swaps two deployment slots of an app.

        Swaps two deployment slots of an app.

        :param resource_group_name: Name of the resource group to which the
         resource belongs.
        :type resource_group_name: str
        :param name: Name of the app.
        :type name: str
        :param slot: Name of the source slot. If a slot is not specified, the
         production slot is used as the source slot.
        :type slot: str
        :param target_slot: Destination deployment slot during swap operation.
        :type target_slot: str
        :param preserve_vnet: <code>true</code> to preserve Virtual Network to
         the slot during swap; otherwise, <code>false</code>.
        :type preserve_vnet: bool
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: The poller return type is ClientRawResponse, the
         direct response alongside the deserialized response
        :param polling: True for ARMPolling, False for no polling, or a
         polling object for personal polling strategy
        :return: An instance of LROPoller that returns None or
         ClientRawResponse<None> if raw==True
        :rtype: ~msrestazure.azure_operation.AzureOperationPoller[None] or
         ~msrestazure.azure_operation.AzureOperationPoller[~msrest.pipeline.ClientRawResponse[None]]
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
    raw_result = self._swap_slot_slot_initial(resource_group_name=resource_group_name, name=name, slot=slot, target_slot=target_slot, preserve_vnet=preserve_vnet, custom_headers=custom_headers, raw=True, **operation_config)

    def get_long_running_output(response):
        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response
    lro_delay = operation_config.get('long_running_operation_timeout', self.config.long_running_operation_timeout)
    if polling is True:
        polling_method = ARMPolling(lro_delay, **operation_config)
    elif polling is False:
        polling_method = NoPolling()
    else:
        polling_method = polling
    return LROPoller(self._client, raw_result, get_long_running_output, polling_method)