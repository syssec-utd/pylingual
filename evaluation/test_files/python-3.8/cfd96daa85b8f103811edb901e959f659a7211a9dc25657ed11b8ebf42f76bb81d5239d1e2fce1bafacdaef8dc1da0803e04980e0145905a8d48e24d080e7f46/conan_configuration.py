from enum import Enum

class ConanConfiguration(str, Enum):
    Debug = ('debug',)
    Release = 'release'
    RelWithDebInfo = 'relwithdebinfo'
    MinSizeRel = 'minsizerel'