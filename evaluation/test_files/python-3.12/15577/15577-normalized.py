def new(cls, access_token, environment='prod'):
    """Create a new storage service REST client.

            Arguments:
                environment: The service environment to be used for the client
                access_token: The access token used to authenticate with the
                    service

            Returns:
                A storage_service.api.ApiClient instance

            Example:
                >>> storage_client = ApiClient.new(my_access_token)

        """
    request = RequestBuilder.request(environment).to_service(cls.SERVICE_NAME, cls.SERVICE_VERSION).throw(StorageForbiddenException, lambda resp: 'You are forbidden to do this.' if resp.status_code == 403 else None).throw(StorageNotFoundException, lambda resp: 'The entity is not found' if resp.status_code == 404 else None).throw(StorageException, lambda resp: 'Server response: {0} - {1}'.format(resp.status_code, resp.text) if not resp.ok else None)
    authenticated_request = request.with_token(access_token)
    return cls(request, authenticated_request)