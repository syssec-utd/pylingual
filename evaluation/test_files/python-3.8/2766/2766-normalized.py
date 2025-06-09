def container_services(self):
    """Instance depends on the API version:

           * 2017-07-01: :class:`ContainerServicesOperations<azure.mgmt.containerservice.v2017_07_01.operations.ContainerServicesOperations>`
        """
    api_version = self._get_api_version('container_services')
    if api_version == '2017-07-01':
        from .v2017_07_01.operations import ContainerServicesOperations as OperationClass
    else:
        raise NotImplementedError('APIVersion {} is not available'.format(api_version))
    return OperationClass(self._client, self.config, Serializer(self._models_dict(api_version)), Deserializer(self._models_dict(api_version)))