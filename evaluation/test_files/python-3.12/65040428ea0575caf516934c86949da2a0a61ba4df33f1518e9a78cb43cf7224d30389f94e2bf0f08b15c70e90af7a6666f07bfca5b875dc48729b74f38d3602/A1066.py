from pyasic.miners._types import Avalon1066
from .A10X import CGMinerA10X

class CGMinerAvalon1066(CGMinerA10X, Avalon1066):

    def __init__(self, ip: str) -> None:
        super().__init__(ip)
        self.ip = ip