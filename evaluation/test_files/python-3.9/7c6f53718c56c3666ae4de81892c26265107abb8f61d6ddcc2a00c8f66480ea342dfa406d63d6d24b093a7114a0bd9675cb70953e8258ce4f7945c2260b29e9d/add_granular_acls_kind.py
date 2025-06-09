from enum import Enum

class AddGranularAclsKind(str, Enum):
    SCRIPT = 'script'
    GROUP = 'group_'
    RESOURCE = 'resource'
    SCHEDULE = 'schedule'
    VARIABLE = 'variable'
    FLOW = 'flow'
    FOLDER = 'folder'
    APP = 'app'

    def __str__(self) -> str:
        return str(self.value)