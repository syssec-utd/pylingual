def get_loggers(self):
    """Return a list of the logger methods: (debug, info, warn, error)"""
    return (self.log.debug, self.log.info, self.log.warn, self.log.error)