def init_extensions(self):
    """Load all IPython extensions in IPythonApp.extensions.

        This uses the :meth:`ExtensionManager.load_extensions` to load all
        the extensions listed in ``self.extensions``.
        """
    try:
        self.log.debug('Loading IPython extensions...')
        extensions = self.default_extensions + self.extensions
        for ext in extensions:
            try:
                self.log.info('Loading IPython extension: %s' % ext)
                self.shell.extension_manager.load_extension(ext)
            except:
                self.log.warn('Error in loading extension: %s' % ext + '\nCheck your config files in %s' % self.profile_dir.location)
                self.shell.showtraceback()
    except:
        self.log.warn('Unknown error in loading extensions:')
        self.shell.showtraceback()