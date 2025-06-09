from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from ......... import repcap

class PeakCls:
    """Peak commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('peak', core, parent)

    def set(self, window=repcap.Window.Default, deltaMarker=repcap.DeltaMarker.Default) -> None:
        """SCPI: CALCulate<n>:DELTamarker<m>:SPECtrogram:Y:MAXimum[:PEAK] 

		Snippet: driver.applications.k60Transient.calculate.deltaMarker.spectrogram.y.maximum.peak.set(window = repcap.Window.Default, deltaMarker = repcap.DeltaMarker.Default) 

		This command moves a delta marker vertically to the highest level for the current frequency. The search includes all
		frames. It does not change the horizontal position of the marker. If the marker hasn't been active yet, the command looks
		for the peak level in the whole spectrogram. 

			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:param deltaMarker: optional repeated capability selector. Default value: Nr1 (settable in the interface 'DeltaMarker')
		"""
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        deltaMarker_cmd_val = self._cmd_group.get_repcap_cmd_value(deltaMarker, repcap.DeltaMarker)
        self._core.io.write(f'CALCulate{window_cmd_val}:DELTamarker{deltaMarker_cmd_val}:SPECtrogram:Y:MAXimum:PEAK')

    def set_with_opc(self, window=repcap.Window.Default, deltaMarker=repcap.DeltaMarker.Default, opc_timeout_ms: int=-1) -> None:
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        deltaMarker_cmd_val = self._cmd_group.get_repcap_cmd_value(deltaMarker, repcap.DeltaMarker)
        "SCPI: CALCulate<n>:DELTamarker<m>:SPECtrogram:Y:MAXimum[:PEAK] \n\n\t\tSnippet: driver.applications.k60Transient.calculate.deltaMarker.spectrogram.y.maximum.peak.set_with_opc(window = repcap.Window.Default, deltaMarker = repcap.DeltaMarker.Default) \n\n\t\tThis command moves a delta marker vertically to the highest level for the current frequency. The search includes all\n\t\tframes. It does not change the horizontal position of the marker. If the marker hasn't been active yet, the command looks\n\t\tfor the peak level in the whole spectrogram. \n\n\t\tSame as set, but waits for the operation to complete before continuing further. Use the RsFsw.utilities.opc_timeout_set() to set the timeout value. \n\n\t\t\t:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')\n\t\t\t:param deltaMarker: optional repeated capability selector. Default value: Nr1 (settable in the interface 'DeltaMarker')\n\t\t\t:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."
        self._core.io.write_with_opc(f'CALCulate{window_cmd_val}:DELTamarker{deltaMarker_cmd_val}:SPECtrogram:Y:MAXimum:PEAK', opc_timeout_ms)