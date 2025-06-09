from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap

class SymbolRateCls:
    """SymbolRate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('symbolRate', core, parent)

    def get(self, outputConnector=repcap.OutputConnector.Default) -> float:
        """SCPI: OUTPut<up>:IQHS:SRATe 

		Snippet: value: float = driver.applications.k60Transient.output.iqhs.symbolRate.get(outputConnector = repcap.OutputConnector.Default) 

		Returns the currently used sample rate to transfer data via the Digital I/Q 40G Streaming Output interface. For details
		on Digital I/Q 40G Streaming Output (R&S FSW-B517/-B1017) , see 'Digital I/Q 40G Streaming Output'. 

			:param outputConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: sample_rate: No help available"""
        outputConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(outputConnector, repcap.OutputConnector)
        response = self._core.io.query_str(f'OUTPut{outputConnector_cmd_val}:IQHS:SRATe?')
        return Conversions.str_to_float(response)