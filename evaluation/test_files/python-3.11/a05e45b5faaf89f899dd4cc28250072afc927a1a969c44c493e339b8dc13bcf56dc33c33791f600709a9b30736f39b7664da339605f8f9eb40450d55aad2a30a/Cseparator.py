from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums

class CseparatorCls:
    """Cseparator commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('cseparator', core, parent)

    def set(self, column_separator: enums.FileSeparator) -> None:
        """SCPI: FORMat:DEXPort:CSEParator 

		Snippet: driver.applications.k40PhaseNoise.formatPy.dexport.cseparator.set(column_separator = enums.FileSeparator.COMMa) 

		No command help available 

			:param column_separator: No help available
		"""
        param = Conversions.enum_scalar_to_str(column_separator, enums.FileSeparator)
        self._core.io.write(f'FORMat:DEXPort:CSEParator {param}')

    def get(self) -> enums.FileSeparator:
        """SCPI: FORMat:DEXPort:CSEParator 

		Snippet: value: enums.FileSeparator = driver.applications.k40PhaseNoise.formatPy.dexport.cseparator.get() 

		No command help available 

			:return: column_separator: No help available"""
        response = self._core.io.query_str(f'FORMat:DEXPort:CSEParator?')
        return Conversions.str_to_scalar_enum(response, enums.FileSeparator)