from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap

class MtableCls:
    """Mtable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('mtable', core, parent)

    def set(self, display_mode: enums.AutoMode, window=repcap.Window.Default) -> None:
        """SCPI: DISPlay[:WINDow<n>]:MTABle 

		Snippet: driver.applications.k40PhaseNoise.display.window.mtable.set(display_mode = enums.AutoMode.AUTO, window = repcap.Window.Default) 

		This command turns the marker table on and off. 

			:param display_mode: ON | 1 Turns on the marker table. OFF | 0 Turns off the marker table. AUTO Turns on the marker table if 3 or more markers are active.
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
		"""
        param = Conversions.enum_scalar_to_str(display_mode, enums.AutoMode)
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        self._core.io.write(f'DISPlay:WINDow{window_cmd_val}:MTABle {param}')

    def get(self, window=repcap.Window.Default) -> enums.AutoMode:
        """SCPI: DISPlay[:WINDow<n>]:MTABle 

		Snippet: value: enums.AutoMode = driver.applications.k40PhaseNoise.display.window.mtable.get(window = repcap.Window.Default) 

		This command turns the marker table on and off. 

			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
			:return: display_mode: ON | 1 Turns on the marker table. OFF | 0 Turns off the marker table. AUTO Turns on the marker table if 3 or more markers are active."""
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        response = self._core.io.query_str(f'DISPlay:WINDow{window_cmd_val}:MTABle?')
        return Conversions.str_to_scalar_enum(response, enums.AutoMode)