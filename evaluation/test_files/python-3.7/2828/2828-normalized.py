def network_watchers(self):
    """Instance depends on the API version:

           * 2016-09-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2016_09_01.operations.NetworkWatchersOperations>`
           * 2016-12-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2016_12_01.operations.NetworkWatchersOperations>`
           * 2017-03-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2017_03_01.operations.NetworkWatchersOperations>`
           * 2017-06-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2017_06_01.operations.NetworkWatchersOperations>`
           * 2017-08-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2017_08_01.operations.NetworkWatchersOperations>`
           * 2017-09-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2017_09_01.operations.NetworkWatchersOperations>`
           * 2017-10-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2017_10_01.operations.NetworkWatchersOperations>`
           * 2017-11-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2017_11_01.operations.NetworkWatchersOperations>`
           * 2018-01-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2018_01_01.operations.NetworkWatchersOperations>`
           * 2018-02-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2018_02_01.operations.NetworkWatchersOperations>`
           * 2018-04-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2018_04_01.operations.NetworkWatchersOperations>`
           * 2018-06-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2018_06_01.operations.NetworkWatchersOperations>`
           * 2018-07-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2018_07_01.operations.NetworkWatchersOperations>`
           * 2018-08-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2018_08_01.operations.NetworkWatchersOperations>`
           * 2018-10-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2018_10_01.operations.NetworkWatchersOperations>`
           * 2018-11-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2018_11_01.operations.NetworkWatchersOperations>`
           * 2018-12-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2018_12_01.operations.NetworkWatchersOperations>`
           * 2019-02-01: :class:`NetworkWatchersOperations<azure.mgmt.network.v2019_02_01.operations.NetworkWatchersOperations>`
        """
    api_version = self._get_api_version('network_watchers')
    if api_version == '2016-09-01':
        from .v2016_09_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2016-12-01':
        from .v2016_12_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2017-03-01':
        from .v2017_03_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2017-06-01':
        from .v2017_06_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2017-08-01':
        from .v2017_08_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2017-09-01':
        from .v2017_09_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2017-10-01':
        from .v2017_10_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2017-11-01':
        from .v2017_11_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2018-01-01':
        from .v2018_01_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2018-02-01':
        from .v2018_02_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2018-04-01':
        from .v2018_04_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2018-06-01':
        from .v2018_06_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2018-07-01':
        from .v2018_07_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2018-08-01':
        from .v2018_08_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2018-10-01':
        from .v2018_10_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2018-11-01':
        from .v2018_11_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2018-12-01':
        from .v2018_12_01.operations import NetworkWatchersOperations as OperationClass
    elif api_version == '2019-02-01':
        from .v2019_02_01.operations import NetworkWatchersOperations as OperationClass
    else:
        raise NotImplementedError('APIVersion {} is not available'.format(api_version))
    return OperationClass(self._client, self.config, Serializer(self._models_dict(api_version)), Deserializer(self._models_dict(api_version)))