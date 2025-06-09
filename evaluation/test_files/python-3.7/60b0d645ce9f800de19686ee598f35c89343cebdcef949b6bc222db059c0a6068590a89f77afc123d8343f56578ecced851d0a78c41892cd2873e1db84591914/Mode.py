from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums

class ModeCls:
    """Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('mode', core, parent)

    def set(self, mode: enums.AutoManualMode) -> None:
        """SCPI: [SENSe]:ADJust:CONFigure:LEVel:DURation:MODE 

		Snippet: driver.applications.k10Xlte.sense.adjust.configure.level.duration.mode.set(mode = enums.AutoManualMode.AUTO) 

		To determine the ideal reference level, the R&S FSW performs a measurement on the current input data.
		This command selects the way the R&S FSW determines the length of the measurement . 

			:param mode: AUTO The R&S FSW determines the measurement length automatically according to the current input data. MANual The R&S FSW uses the measurement length defined by [SENSe:]ADJust:CONFigure:LEVel:DURation.
		"""
        param = Conversions.enum_scalar_to_str(mode, enums.AutoManualMode)
        self._core.io.write(f'SENSe:ADJust:CONFigure:LEVel:DURation:MODE {param}')

    def get(self) -> enums.AutoManualMode:
        """SCPI: [SENSe]:ADJust:CONFigure:LEVel:DURation:MODE 

		Snippet: value: enums.AutoManualMode = driver.applications.k10Xlte.sense.adjust.configure.level.duration.mode.get() 

		To determine the ideal reference level, the R&S FSW performs a measurement on the current input data.
		This command selects the way the R&S FSW determines the length of the measurement . 

			:return: mode: AUTO The R&S FSW determines the measurement length automatically according to the current input data. MANual The R&S FSW uses the measurement length defined by [SENSe:]ADJust:CONFigure:LEVel:DURation."""
        response = self._core.io.query_str(f'SENSe:ADJust:CONFigure:LEVel:DURation:MODE?')
        return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)