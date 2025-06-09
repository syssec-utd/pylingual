def find_module(self, module_name, path=None):
    """
        Searches the paths for the required module.

        :param module_name: the full name of the module to find
        :param path: set to None when the module in being searched for is a
                     top-level module - otherwise this is set to
                     package.__path__ for submodules and subpackages (unused)
        """
    module_path = os.path.join(*module_name.split(MODULE_PATH_SEP))
    for search_root in self.paths:
        target_path = os.path.join(search_root, module_path)
        is_pkg = False
        if os.path.isdir(target_path):
            target_file = os.path.join(target_path, '__init__.py')
            is_pkg = True
        else:
            target_file = '{}.py'.format(target_path)
        if os.path.exists(target_file):
            return ModuleLoader(target_path, module_name, target_file, is_pkg)
    return None