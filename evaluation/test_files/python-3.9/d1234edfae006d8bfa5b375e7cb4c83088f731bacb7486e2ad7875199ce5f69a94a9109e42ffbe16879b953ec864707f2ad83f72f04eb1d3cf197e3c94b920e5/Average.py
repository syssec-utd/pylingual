from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap

class AverageCls:
    """Average commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('average', core, parent)

    def get(self, window=repcap.Window.Default) -> float:
        """SCPI: FETCh<n>:SUMMary:EVM:SHR:NRMSe:AVERage 

		Snippet: value: float = driver.applications.k149Uwb.fetch.summary.evm.shr.nrmse.average.get(window = repcap.Window.Default) 

		No command help available 

			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fetch')
			:return: result: numeric value"""
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        response = self._core.io.query_str(f'FETCh{window_cmd_val}:SUMMary:EVM:SHR:NRMSe:AVERage?')
        return Conversions.str_to_float(response)