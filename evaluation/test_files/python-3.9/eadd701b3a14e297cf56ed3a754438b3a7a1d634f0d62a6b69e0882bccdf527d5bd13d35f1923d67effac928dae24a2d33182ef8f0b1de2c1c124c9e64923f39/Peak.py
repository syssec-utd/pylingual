from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from ....... import repcap

class PeakCls:
    """Peak commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('peak', core, parent)

    def set(self, window=repcap.Window.Default, deltaMarker=repcap.DeltaMarker.Default) -> None:
        """SCPI: CALCulate<n>:DELTamarker<m>:SPECtrogram:XY:MAXimum[:PEAK] 

		Snippet: driver.calculate.deltaMarker.spectrogram.xy.maximum.peak.set(window = repcap.Window.Default, deltaMarker = repcap.DeltaMarker.Default) 

		This command moves a marker to the highest level of the spectrogram over all frequencies. 

			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:param deltaMarker: optional repeated capability selector. Default value: Nr1 (settable in the interface 'DeltaMarker')
		"""
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        deltaMarker_cmd_val = self._cmd_group.get_repcap_cmd_value(deltaMarker, repcap.DeltaMarker)
        self._core.io.write(f'CALCulate{window_cmd_val}:DELTamarker{deltaMarker_cmd_val}:SPECtrogram:XY:MAXimum:PEAK')

    def set_with_opc(self, window=repcap.Window.Default, deltaMarker=repcap.DeltaMarker.Default, opc_timeout_ms: int=-1) -> None:
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        deltaMarker_cmd_val = self._cmd_group.get_repcap_cmd_value(deltaMarker, repcap.DeltaMarker)
        "SCPI: CALCulate<n>:DELTamarker<m>:SPECtrogram:XY:MAXimum[:PEAK] \n\n\t\tSnippet: driver.calculate.deltaMarker.spectrogram.xy.maximum.peak.set_with_opc(window = repcap.Window.Default, deltaMarker = repcap.DeltaMarker.Default) \n\n\t\tThis command moves a marker to the highest level of the spectrogram over all frequencies. \n\n\t\tSame as set, but waits for the operation to complete before continuing further. Use the RsFsw.utilities.opc_timeout_set() to set the timeout value. \n\n\t\t\t:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')\n\t\t\t:param deltaMarker: optional repeated capability selector. Default value: Nr1 (settable in the interface 'DeltaMarker')\n\t\t\t:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."
        self._core.io.write_with_opc(f'CALCulate{window_cmd_val}:DELTamarker{deltaMarker_cmd_val}:SPECtrogram:XY:MAXimum:PEAK', opc_timeout_ms)