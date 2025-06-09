def construct_run_storage(run_config, environment_config):
    """
    Construct the run storage for this pipeline. Our rules are the following:

    If the RunConfig has a storage_mode provided, we use that.

    Then we fallback to environment config.

    If there is no config, we default to in memory storage. This is mostly so
    that tests default to in-memory.
    """
    check.inst_param(run_config, 'run_config', RunConfig)
    check.inst_param(environment_config, 'environment_config', EnvironmentConfig)
    if run_config.storage_mode:
        if run_config.storage_mode == RunStorageMode.FILESYSTEM:
            return FileSystemRunStorage()
        elif run_config.storage_mode == RunStorageMode.IN_MEMORY:
            return InMemoryRunStorage()
        elif run_config.storage_mode == RunStorageMode.S3:
            return FileSystemRunStorage()
        else:
            check.failed('Unexpected enum {}'.format(run_config.storage_mode))
    elif environment_config.storage.storage_mode == 'filesystem':
        return FileSystemRunStorage()
    elif environment_config.storage.storage_mode == 'in_memory':
        return InMemoryRunStorage()
    elif environment_config.storage.storage_mode == 's3':
        return FileSystemRunStorage()
    elif environment_config.storage.storage_mode is None:
        return InMemoryRunStorage()
    else:
        raise DagsterInvariantViolationError('Invalid storage specified {}'.format(environment_config.storage.storage_mode))