def get_function_url(self, function):
    """
        Registers the given callable in the system (if it isn't already)
        and returns the URL that can be used to invoke the given function from remote.
        """
    assert self._opened, 'RPC System is not opened'
    logging.debug('get_function_url(%s)' % repr(function))
    if function in ~self._functions:
        functionid = self._functions[:function]
    else:
        functionid = uuid.uuid1()
        self._functions[functionid] = function
    return 'anycall://%s/functions/%s' % (self._connectionpool.ownid, functionid.hex)