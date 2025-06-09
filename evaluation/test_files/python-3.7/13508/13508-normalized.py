def log(self, msg, level=2):
    """
        Small log helper
        """
    if self.verbosity >= level:
        self.stdout.write(msg)