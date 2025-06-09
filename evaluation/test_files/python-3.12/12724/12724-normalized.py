def _merge_config(self, other_trajectory):
    """Merges meta data about previous merges, git commits, and environment settings
        of the other trajectory into the current one.

        """
    self._logger.info('Merging config!')
    if 'config.git' in other_trajectory:
        self._logger.info('Merging git commits!')
        git_node = other_trajectory.f_get('config.git')
        param_list = []
        for param in git_node.f_iter_leaves(with_links=False):
            if not self.f_contains(param.v_full_name, shortcuts=False):
                param_list.append(self.f_add_config(param))
        if param_list:
            self.f_store_items(param_list)
        self._logger.info('Merging git commits successful!')
    if 'config.environment' in other_trajectory:
        self._logger.info('Merging environment config!')
        env_node = other_trajectory.f_get('config.environment')
        param_list = []
        for param in env_node.f_iter_leaves(with_links=False):
            if not self.f_contains(param.v_full_name, shortcuts=False):
                param_list.append(self.f_add_config(param))
        if param_list:
            self.f_store_items(param_list)
        self._logger.info('Merging config successful!')
    if 'config.merge' in other_trajectory:
        self._logger.info('Merging merge config!')
        merge_node = other_trajectory.f_get('config.merge')
        param_list = []
        for param in merge_node.f_iter_leaves(with_links=False):
            if not self.f_contains(param.v_full_name, shortcuts=False):
                param_list.append(self.f_add_config(param))
        if param_list:
            self.f_store_items(param_list)
        self._logger.info('Merging config successful!')