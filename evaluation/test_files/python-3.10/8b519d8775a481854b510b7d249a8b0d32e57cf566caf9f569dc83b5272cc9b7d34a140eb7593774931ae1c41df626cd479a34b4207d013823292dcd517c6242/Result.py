from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions

class ResultCls:
    """Result commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('result', core, parent)

    def get(self) -> float:
        """SCPI: FETCh:PTABle:P2DB:MAXimum:Y[:RESult] 

		Snippet: value: float = driver.applications.k18AmplifierEt.fetch.ptable.p2Db.maximum.y.result.get() 

		These commands query the result values for the 2 dB Compression Point result as shown in the 'Parameter Sweep' Table. 

			:return: results: numeric value • For ...[:RESult]: Minimum or maximum result that has been measured. • For ...:X[:RESult]: Location on the x-axis where the minimum or maximum result has been measured. The type of value depends on the parameter you have selected for the x-axis (method RsFsw.Applications.K18_AmplifierEt.Configure.Psweep.X.Setting.set) . • For ...:Y[:RESult]: Location on the y-axis where the minimum or maximum result has been measured. The type of value depends on the parameter you have selected for the y-axis (method RsFsw.Applications.K18_AmplifierEt.Configure.Psweep.Y.Setting.set) ."""
        response = self._core.io.query_str(f'FETCh:PTABle:P2DB:MAXimum:Y:RESult?')
        return Conversions.str_to_float(response)