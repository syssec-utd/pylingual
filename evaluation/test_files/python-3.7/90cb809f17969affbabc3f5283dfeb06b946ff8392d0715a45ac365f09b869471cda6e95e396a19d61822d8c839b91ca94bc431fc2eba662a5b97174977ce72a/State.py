from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap

class StateCls:
    """State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('state', core, parent)

    def set(self, state: bool, window=repcap.Window.Default, freqLine=repcap.FreqLine.Default) -> None:
        """SCPI: CALCulate<n>:FLINe<dl>:STATe 

		Snippet: driver.applications.k91Wlan.calculate.fline.state.set(state = False, window = repcap.Window.Default, freqLine = repcap.FreqLine.Default) 

		No command help available 

			:param state: No help available
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:param freqLine: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fline')
		"""
        param = Conversions.bool_to_str(state)
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        freqLine_cmd_val = self._cmd_group.get_repcap_cmd_value(freqLine, repcap.FreqLine)
        self._core.io.write(f'CALCulate{window_cmd_val}:FLINe{freqLine_cmd_val}:STATe {param}')

    def get(self, window=repcap.Window.Default, freqLine=repcap.FreqLine.Default) -> bool:
        """SCPI: CALCulate<n>:FLINe<dl>:STATe 

		Snippet: value: bool = driver.applications.k91Wlan.calculate.fline.state.get(window = repcap.Window.Default, freqLine = repcap.FreqLine.Default) 

		No command help available 

			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:param freqLine: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fline')
			:return: state: No help available"""
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        freqLine_cmd_val = self._cmd_group.get_repcap_cmd_value(freqLine, repcap.FreqLine)
        response = self._core.io.query_str(f'CALCulate{window_cmd_val}:FLINe{freqLine_cmd_val}:STATe?')
        return Conversions.str_to_bool(response)