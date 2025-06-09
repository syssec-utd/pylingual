def import_key(self, vault_base_url, key_name, key, hsm=None, key_attributes=None, tags=None, custom_headers=None, raw=False, **operation_config):
    """Imports an externally created key, stores it, and returns key
        parameters and attributes to the client.

        The import key operation may be used to import any key type into an
        Azure Key Vault. If the named key already exists, Azure Key Vault
        creates a new version of the key. This operation requires the
        keys/import permission.

        :param vault_base_url: The vault name, for example
         https://myvault.vault.azure.net.
        :type vault_base_url: str
        :param key_name: Name for the imported key.
        :type key_name: str
        :param key: The Json web key
        :type key: ~azure.keyvault.v2016_10_01.models.JsonWebKey
        :param hsm: Whether to import as a hardware key (HSM) or software key.
        :type hsm: bool
        :param key_attributes: The key management attributes.
        :type key_attributes: ~azure.keyvault.v2016_10_01.models.KeyAttributes
        :param tags: Application specific metadata in the form of key-value
         pairs.
        :type tags: dict[str, str]
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: KeyBundle or ClientRawResponse if raw=true
        :rtype: ~azure.keyvault.v2016_10_01.models.KeyBundle or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`KeyVaultErrorException<azure.keyvault.v2016_10_01.models.KeyVaultErrorException>`
        """
    parameters = models.KeyImportParameters(hsm=hsm, key=key, key_attributes=key_attributes, tags=tags)
    url = self.import_key.metadata['url']
    path_format_arguments = {'vaultBaseUrl': self._serialize.url('vault_base_url', vault_base_url, 'str', skip_quote=True), 'key-name': self._serialize.url('key_name', key_name, 'str', pattern='^[0-9a-zA-Z-]+$')}
    url = self._client.format_url(url, **path_format_arguments)
    query_parameters = {}
    query_parameters['api-version'] = self._serialize.query('self.api_version', self.api_version, 'str')
    header_parameters = {}
    header_parameters['Content-Type'] = 'application/json; charset=utf-8'
    if self.config.generate_client_request_id:
        header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
    if custom_headers:
        header_parameters.update(custom_headers)
    if self.config.accept_language is not None:
        header_parameters['accept-language'] = self._serialize.header('self.config.accept_language', self.config.accept_language, 'str')
    body_content = self._serialize.body(parameters, 'KeyImportParameters')
    request = self._client.put(url, query_parameters)
    response = self._client.send(request, header_parameters, body_content, stream=False, **operation_config)
    if response.status_code not in [200]:
        raise models.KeyVaultErrorException(self._deserialize, response)
    deserialized = None
    if response.status_code == 200:
        deserialized = self._deserialize('KeyBundle', response)
    if raw:
        client_raw_response = ClientRawResponse(deserialized, response)
        return client_raw_response
    return deserialized