from typing import List
from ert._c_wrappers.enkf.enums import RealizationStateEnum
from ert._clib.state_map import StateMap

def __getitem__(self, iens: int) -> RealizationStateEnum:
    return self._get(iens)

def __iter__(self):
    index = 0
    size = len(self)
    while index < size:
        yield self[index]
        index += 1

def realizationList(self, state_value: RealizationStateEnum) -> List[int]:
    """Will create an integer list of all realisations with state equal to
    state_value."""
    mask = self.createMask(state_value)
    return [idx for idx, value in enumerate(mask) if value]

def createMask(self, state_value: RealizationStateEnum) -> List[bool]:
    """Will create a bool list of all realisations with state equal to
    state_value."""
    return self.selectMatching(state_value)
StateMap.__getitem__ = __getitem__
StateMap.__iter__ = __iter__
StateMap.realizationList = realizationList
StateMap.createMask = createMask
del __getitem__
del __iter__
del realizationList
del createMask
__all__ = ['StateMap', 'RealizationStateEnum']