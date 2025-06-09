def _register_extension(self, name, ext):
    """register extension

        :param name: extension name
        :param ext: extension object
        """
    ext.init_app(self)
    if name in self._extensions:
        raise exceptions.ConfigException('extension duplicated: {}'.format(name))
    self._extensions[name] = ext