def setCodeVersion(self, newVersion, callback=None):
    """Switch to a new code version on all cluster nodes. You
        should ensure that cluster nodes are updated, otherwise they
        won't be able to apply commands.

        :param newVersion: new code version
        :type int
        :param callback: will be called on cussess or fail
        :type callback: function(`FAIL_REASON <#pysyncobj.FAIL_REASON>`_, None)
        """
    assert isinstance(newVersion, int)
    if newVersion > self.__selfCodeVersion:
        raise Exception('wrong version, current version is %d, requested version is %d' % (self.__selfCodeVersion, newVersion))
    if newVersion < self.__enabledCodeVersion:
        raise Exception('wrong version, enabled version is %d, requested version is %d' % (self.__enabledCodeVersion, newVersion))
    self._applyCommand(pickle.dumps(newVersion), callback, _COMMAND_TYPE.VERSION)