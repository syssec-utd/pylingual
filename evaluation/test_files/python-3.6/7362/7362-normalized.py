def from_object(cls: Type['Config'], instance: Union[object, str]) -> 'Config':
    """Create a configuration from a Python object.

        This can be used to reference modules or objects within
        modules for example,

        .. code-block:: python

            Config.from_object('module')
            Config.from_object('module.instance')
            from module import instance
            Config.from_object(instance)

        are valid.

        Arguments:
            instance: Either a str referencing a python object or the
                object itself.

        """
    if isinstance(instance, str):
        try:
            (path, config) = instance.rsplit('.', 1)
        except ValueError:
            path = instance
            instance = importlib.import_module(instance)
        else:
            module = importlib.import_module(path)
            instance = getattr(module, config)
    mapping = {key: getattr(instance, key) for key in dir(instance) if not isinstance(getattr(instance, key), types.ModuleType)}
    return cls.from_mapping(mapping)