def printStatus(self):
    """Dumps different debug info about cluster to default logger"""
    status = self.getStatus()
    for (k, v) in iteritems(status):
        logging.info('%s: %s' % (str(k), str(v)))