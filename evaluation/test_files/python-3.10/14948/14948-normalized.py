def setup(self, data_manager):
    """
        Hook to setup this service with a specific DataManager.

        Will recursively setup sub-services.
        """
    self._data_manager = data_manager
    if self._data_manager:
        self._dal = self._data_manager.get_dal()
    else:
        self._dal = None
    for (key, service) in self._services.items():
        service.setup(self._data_manager)