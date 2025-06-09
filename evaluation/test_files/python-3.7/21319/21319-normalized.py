def configure(self, options, conf):
    """Configure plugin. Plugin is enabled by default.
        """
    self.conf = conf
    if not options.capture:
        self.enabled = False