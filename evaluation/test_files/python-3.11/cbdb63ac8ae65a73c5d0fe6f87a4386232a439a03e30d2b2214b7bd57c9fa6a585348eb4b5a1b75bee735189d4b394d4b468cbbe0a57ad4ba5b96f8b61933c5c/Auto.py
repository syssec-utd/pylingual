from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions

class AutoCls:
    """Auto commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('auto', core, parent)

    def set(self, state: bool) -> None:
        """SCPI: INPut:DIQ:SRATe:AUTO 

		Snippet: driver.inputPy.diq.symbolRate.auto.set(state = False) 

		If enabled, the sample rate of the digital I/Q input signal is set automatically by the connected device. This command is
		only available if the optional 'Digital Baseband' interface is installed. 

			:param state: ON | OFF | 1 | 0
		"""
        param = Conversions.bool_to_str(state)
        self._core.io.write(f'INPut:DIQ:SRATe:AUTO {param}')