def plugins(self):
    """
        :returns: {plugin_name: plugin_class, ...}
        :rtype: dict
        """
    if self._plugins is None:
        self.load_plugins()
        if self._plugins is None:
            self._plugins = {}
    return self._plugins