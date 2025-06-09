def features(self):
    """Instance depends on the API version:

           * 2015-12-01: :class:`FeaturesOperations<azure.mgmt.resource.features.v2015_12_01.operations.FeaturesOperations>`
        """
    api_version = self._get_api_version('features')
    if api_version == '2015-12-01':
        from .v2015_12_01.operations import FeaturesOperations as OperationClass
    else:
        raise NotImplementedError('APIVersion {} is not available'.format(api_version))
    return OperationClass(self._client, self.config, Serializer(self._models_dict(api_version)), Deserializer(self._models_dict(api_version)))