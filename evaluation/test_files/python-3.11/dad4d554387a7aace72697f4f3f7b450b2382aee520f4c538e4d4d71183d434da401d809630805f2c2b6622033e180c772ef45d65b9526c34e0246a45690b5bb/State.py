from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions

class StateCls:
    """State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('state', core, parent)

    def set(self, state: bool) -> None:
        """SCPI: [SENSe]:POWer:NCORrection:CALibration:STATe 

		Snippet: driver.sense.power.ncorrection.calibration.state.set(state = False) 

		No command help available 

			:param state: No help available
		"""
        param = Conversions.bool_to_str(state)
        self._core.io.write(f'SENSe:POWer:NCORrection:CALibration:STATe {param}')

    def get(self) -> bool:
        """SCPI: [SENSe]:POWer:NCORrection:CALibration:STATe 

		Snippet: value: bool = driver.sense.power.ncorrection.calibration.state.get() 

		No command help available 

			:return: state: No help available"""
        response = self._core.io.query_str(f'SENSe:POWer:NCORrection:CALibration:STATe?')
        return Conversions.str_to_bool(response)