def make_config(self, instance_relative=False):
    """Used to create the config attribute by the Flask constructor.
        The `instance_relative` parameter is passed in from the constructor
        of Flask (there named `instance_relative_config`) and indicates if
        the config should be relative to the instance path or the root path
        of the application.

        .. versionadded:: 0.8
        """
    root_path = self.root_path
    if instance_relative:
        root_path = self.instance_path
    return Config(root_path, self.default_config)