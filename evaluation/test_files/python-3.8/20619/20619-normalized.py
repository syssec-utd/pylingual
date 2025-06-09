def load_config_file(self, filename, path=None):
    """Load a .py based config file by filename and path."""
    loader = PyFileConfigLoader(filename, path=path)
    try:
        config = loader.load_config()
    except ConfigFileNotFound:
        raise
    except Exception:
        filename = loader.full_filename or filename
        self.log.error('Exception while loading config file %s', filename, exc_info=True)
    else:
        self.log.debug('Loaded config file: %s', loader.full_filename)
        self.update_config(config)