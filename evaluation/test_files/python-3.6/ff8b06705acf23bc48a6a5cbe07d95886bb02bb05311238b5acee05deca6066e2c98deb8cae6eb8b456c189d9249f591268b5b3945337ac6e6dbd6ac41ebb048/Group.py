from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap

class GroupCls:
    """Group commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('group', core, parent)

    def set(self, group: int, window=repcap.Window.Default) -> None:
        """SCPI: SENSe[:WINDow<n>]:DISPlay:RWConfig:GROup 

		Snippet: driver.applications.k149Uwb.sense.window.display.rwConfig.group.set(group = 1, window = repcap.Window.Default) 

		Sets the Group for this window and for any windows this window is linked to. 

			:param group: 1..n Window
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
		"""
        param = Conversions.decimal_value_to_str(group)
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        self._core.io.write(f'SENSe:WINDow{window_cmd_val}:DISPlay:RWConfig:GROup {param}')

    def get(self, window=repcap.Window.Default) -> int:
        """SCPI: SENSe[:WINDow<n>]:DISPlay:RWConfig:GROup 

		Snippet: value: int = driver.applications.k149Uwb.sense.window.display.rwConfig.group.get(window = repcap.Window.Default) 

		Sets the Group for this window and for any windows this window is linked to. 

			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
			:return: group: No help available"""
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        response = self._core.io.query_str(f'SENSe:WINDow{window_cmd_val}:DISPlay:RWConfig:GROup?')
        return Conversions.str_to_int(response)