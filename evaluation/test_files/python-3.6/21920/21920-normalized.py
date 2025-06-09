def configure(self, options, config):
    """Configures the xunit plugin."""
    Plugin.configure(self, options, config)
    self.config = config
    if self.enabled:
        self.stats = {'errors': 0, 'failures': 0, 'passes': 0, 'skipped': 0}
        self.errorlist = []
        self.error_report_file = codecs.open(options.xunit_file, 'w', self.encoding, 'replace')