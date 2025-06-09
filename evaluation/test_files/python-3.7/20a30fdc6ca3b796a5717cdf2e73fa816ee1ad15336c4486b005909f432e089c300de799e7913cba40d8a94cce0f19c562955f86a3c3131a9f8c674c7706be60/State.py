from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap

class StateCls:
    """State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('state', core, parent)

    def set(self, arg_0: bool, powerMeter=repcap.PowerMeter.Default) -> None:
        """SCPI: [SENSe]:PMETer<p>:MTIMe:AVERage[:STATe] 

		Snippet: driver.applications.k9X11Ad.sense.pmeter.mtime.average.state.set(arg_0 = False, powerMeter = repcap.PowerMeter.Default) 

		No command help available 

			:param arg_0: No help available
			:param powerMeter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmeter')
		"""
        param = Conversions.bool_to_str(arg_0)
        powerMeter_cmd_val = self._cmd_group.get_repcap_cmd_value(powerMeter, repcap.PowerMeter)
        self._core.io.write(f'SENSe:PMETer{powerMeter_cmd_val}:MTIMe:AVERage:STATe {param}')

    def get(self, powerMeter=repcap.PowerMeter.Default) -> bool:
        """SCPI: [SENSe]:PMETer<p>:MTIMe:AVERage[:STATe] 

		Snippet: value: bool = driver.applications.k9X11Ad.sense.pmeter.mtime.average.state.get(powerMeter = repcap.PowerMeter.Default) 

		No command help available 

			:param powerMeter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmeter')
			:return: arg_0: No help available"""
        powerMeter_cmd_val = self._cmd_group.get_repcap_cmd_value(powerMeter, repcap.PowerMeter)
        response = self._core.io.query_str(f'SENSe:PMETer{powerMeter_cmd_val}:MTIMe:AVERage:STATe?')
        return Conversions.str_to_bool(response)