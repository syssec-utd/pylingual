def set_value(self, key, value):
    """
        Set a value within the configuration based on its key. The key
        may be nested, any nested levels that do not exist prior to the final
        segment of the key path will be created.
        *Note*: In order to write changes to the file, ensure that
        :meth:`~giraffez.config.Config.write` is called prior to exit.

        :param str key: A path to the value destination, with nested levels joined by '.'
        :param value: Value to set at the given key, can be any value that is
            YAML serializeable.
        """
    if key.endswith('.'):
        key = key[:-1]
    path = key.split('.')
    curr = self.settings
    for p in path[:-1]:
        if p not in curr:
            curr[p] = {}
        curr = curr[p]
    if not isinstance(curr, dict):
        raise ConfigurationError("Cannot set nested key '{}' in configuration value '{}' (destination is not a dictionary).".format(path[-1], key))
    value = self.encrypt(value, path)
    if value in {'true', 'True'}:
        value = True
    if value in {'false', 'False'}:
        value = False
    curr[path[-1]] = value