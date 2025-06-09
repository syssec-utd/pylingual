def update_policies(self, resource_group_name, registry_name, quarantine_policy=None, trust_policy=None, custom_headers=None, raw=False, polling=True, **operation_config):
    """Updates the policies for the specified container registry.

        :param resource_group_name: The name of the resource group to which
         the container registry belongs.
        :type resource_group_name: str
        :param registry_name: The name of the container registry.
        :type registry_name: str
        :param quarantine_policy: An object that represents quarantine policy
         for a container registry.
        :type quarantine_policy:
         ~azure.mgmt.containerregistry.v2018_02_01_preview.models.QuarantinePolicy
        :param trust_policy: An object that represents content trust policy
         for a container registry.
        :type trust_policy:
         ~azure.mgmt.containerregistry.v2018_02_01_preview.models.TrustPolicy
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: The poller return type is ClientRawResponse, the
         direct response alongside the deserialized response
        :param polling: True for ARMPolling, False for no polling, or a
         polling object for personal polling strategy
        :return: An instance of LROPoller that returns RegistryPolicies or
         ClientRawResponse<RegistryPolicies> if raw==True
        :rtype:
         ~msrestazure.azure_operation.AzureOperationPoller[~azure.mgmt.containerregistry.v2018_02_01_preview.models.RegistryPolicies]
         or
         ~msrestazure.azure_operation.AzureOperationPoller[~msrest.pipeline.ClientRawResponse[~azure.mgmt.containerregistry.v2018_02_01_preview.models.RegistryPolicies]]
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
    raw_result = self._update_policies_initial(resource_group_name=resource_group_name, registry_name=registry_name, quarantine_policy=quarantine_policy, trust_policy=trust_policy, custom_headers=custom_headers, raw=True, **operation_config)

    def get_long_running_output(response):
        deserialized = self._deserialize('RegistryPolicies', response)
        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response
        return deserialized
    lro_delay = operation_config.get('long_running_operation_timeout', self.config.long_running_operation_timeout)
    if polling is True:
        polling_method = ARMPolling(lro_delay, **operation_config)
    elif polling is False:
        polling_method = NoPolling()
    else:
        polling_method = polling
    return LROPoller(self._client, raw_result, get_long_running_output, polling_method)