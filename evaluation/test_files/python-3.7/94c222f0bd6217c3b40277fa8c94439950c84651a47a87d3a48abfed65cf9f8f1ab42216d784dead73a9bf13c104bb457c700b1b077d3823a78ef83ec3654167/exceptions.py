class MasterNotAvailableException(Exception):
    pass

class MasterTemporarilyNotAvailableException(Exception):
    pass

class NoSlavesAvailableError(Exception):
    pass

class MultipleSlavesForIDError(Exception):
    pass

class TaskNotFoundException(Exception):
    pass

class FileNotFoundForTaskException(Exception):
    pass

class MultipleTasksForIDError(Exception):
    pass

class FileDoesNotExist(Exception):
    pass

class MissingExecutor(Exception):
    pass

class SlaveDoesNotExist(Exception):
    pass

class SkipResult(Exception):
    pass