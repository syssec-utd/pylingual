from pyasic.miners._backends import CGMiner
from pyasic.miners._types import S17Plus

class CGMinerS17Plus(CGMiner, S17Plus):

    def __init__(self, ip: str) -> None:
        super().__init__(ip)
        self.ip = ip