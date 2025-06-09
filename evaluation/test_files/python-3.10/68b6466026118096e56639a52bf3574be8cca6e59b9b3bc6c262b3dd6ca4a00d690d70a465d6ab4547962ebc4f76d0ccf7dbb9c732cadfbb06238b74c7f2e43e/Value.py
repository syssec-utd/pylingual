from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions

class ValueCls:
    """Value commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('value', core, parent)

    def set(self, reference_value: float) -> None:
        """SCPI: CONFigure:CMEasurement:REFerence:VALue 

		Snippet: driver.configure.cmeasurement.reference.value.set(reference_value = 1.0) 

		No command help available 

			:param reference_value: No help available
		"""
        param = Conversions.decimal_value_to_str(reference_value)
        self._core.io.write(f'CONFigure:CMEasurement:REFerence:VALue {param}')

    def get(self) -> float:
        """SCPI: CONFigure:CMEasurement:REFerence:VALue 

		Snippet: value: float = driver.configure.cmeasurement.reference.value.get() 

		No command help available 

			:return: reference_value: No help available"""
        response = self._core.io.query_str(f'CONFigure:CMEasurement:REFerence:VALue?')
        return Conversions.str_to_float(response)