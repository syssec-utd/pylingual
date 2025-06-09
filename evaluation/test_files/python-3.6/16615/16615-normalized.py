def abort(self, signum):
    """ Run all abort tasks, then all exit tasks, then exit with error
        return status"""
    self.log.info('Signal handler received abort request')
    self._abort(signum)
    self._exit(signum)
    os._exit(1)