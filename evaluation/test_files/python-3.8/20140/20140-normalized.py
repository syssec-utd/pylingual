def run(self, result):
    """Run tests in suite inside of suite fixtures.
        """
    log.debug('suite %s (%s) run called, tests: %s', id(self), self, self._tests)
    if self.resultProxy:
        (result, orig) = (self.resultProxy(result, self), result)
    else:
        (result, orig) = (result, result)
    try:
        self.setUp()
    except KeyboardInterrupt:
        raise
    except:
        self.error_context = 'setup'
        result.addError(self, self._exc_info())
        return
    try:
        for test in self._tests:
            if result.shouldStop:
                log.debug('stopping')
                break
            test(orig)
    finally:
        self.has_run = True
        try:
            self.tearDown()
        except KeyboardInterrupt:
            raise
        except:
            self.error_context = 'teardown'
            result.addError(self, self._exc_info())