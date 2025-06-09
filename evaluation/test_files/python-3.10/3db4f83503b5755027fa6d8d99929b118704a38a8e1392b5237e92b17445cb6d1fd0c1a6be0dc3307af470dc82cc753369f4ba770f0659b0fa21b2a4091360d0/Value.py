from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap

class ValueCls:
    """Value commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('value', core, parent)

    def set(self, arg_0: float, powerMeter=repcap.PowerMeter.Default) -> None:
        """SCPI: [SENSe]:PMETer<p>:DCYCle:VALue 

		Snippet: driver.applications.k9X11Ad.sense.pmeter.dcycle.value.set(arg_0 = 1.0, powerMeter = repcap.PowerMeter.Default) 

		No command help available 

			:param arg_0: No help available
			:param powerMeter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmeter')
		"""
        param = Conversions.decimal_value_to_str(arg_0)
        powerMeter_cmd_val = self._cmd_group.get_repcap_cmd_value(powerMeter, repcap.PowerMeter)
        self._core.io.write(f'SENSe:PMETer{powerMeter_cmd_val}:DCYCle:VALue {param}')

    def get(self, powerMeter=repcap.PowerMeter.Default) -> float:
        """SCPI: [SENSe]:PMETer<p>:DCYCle:VALue 

		Snippet: value: float = driver.applications.k9X11Ad.sense.pmeter.dcycle.value.get(powerMeter = repcap.PowerMeter.Default) 

		No command help available 

			:param powerMeter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmeter')
			:return: arg_0: No help available"""
        powerMeter_cmd_val = self._cmd_group.get_repcap_cmd_value(powerMeter, repcap.PowerMeter)
        response = self._core.io.query_str(f'SENSe:PMETer{powerMeter_cmd_val}:DCYCle:VALue?')
        return Conversions.str_to_float(response)