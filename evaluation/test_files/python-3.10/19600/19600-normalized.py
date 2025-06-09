def import_modules(self):
    """Import customer's service module."""
    modules = self.get_modules()
    log.info('import service modules: ' + str(modules))
    try:
        for module in modules:
            __import__(module)
    except ImportError as error:
        raise ImportModulesError(error.msg)