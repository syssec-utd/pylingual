def resource_groups(self):
    """Instance depends on the API version:

           * 2016-02-01: :class:`ResourceGroupsOperations<azure.mgmt.resource.resources.v2016_02_01.operations.ResourceGroupsOperations>`
           * 2016-09-01: :class:`ResourceGroupsOperations<azure.mgmt.resource.resources.v2016_09_01.operations.ResourceGroupsOperations>`
           * 2017-05-10: :class:`ResourceGroupsOperations<azure.mgmt.resource.resources.v2017_05_10.operations.ResourceGroupsOperations>`
           * 2018-02-01: :class:`ResourceGroupsOperations<azure.mgmt.resource.resources.v2018_02_01.operations.ResourceGroupsOperations>`
           * 2018-05-01: :class:`ResourceGroupsOperations<azure.mgmt.resource.resources.v2018_05_01.operations.ResourceGroupsOperations>`
        """
    api_version = self._get_api_version('resource_groups')
    if api_version == '2016-02-01':
        from .v2016_02_01.operations import ResourceGroupsOperations as OperationClass
    elif api_version == '2016-09-01':
        from .v2016_09_01.operations import ResourceGroupsOperations as OperationClass
    elif api_version == '2017-05-10':
        from .v2017_05_10.operations import ResourceGroupsOperations as OperationClass
    elif api_version == '2018-02-01':
        from .v2018_02_01.operations import ResourceGroupsOperations as OperationClass
    elif api_version == '2018-05-01':
        from .v2018_05_01.operations import ResourceGroupsOperations as OperationClass
    else:
        raise NotImplementedError('APIVersion {} is not available'.format(api_version))
    return OperationClass(self._client, self.config, Serializer(self._models_dict(api_version)), Deserializer(self._models_dict(api_version)))