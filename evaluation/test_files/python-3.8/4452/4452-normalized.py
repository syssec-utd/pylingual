def publish(self, key, value):
    """publish value to status"""
    self.log.debug('Publishing status: %s/%s: %s', self.__class__.__name__, key, value)
    self.core.publish(self.__class__.__name__, key, value)