def initialize_options(self):
    """Set the default options."""
    self.branch = 'master'
    self.fix = False
    super(lint, self).initialize_options()