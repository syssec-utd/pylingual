from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ...........Internal.Types import DataType
from ...........Internal.ArgSingleList import ArgSingleList
from ...........Internal.ArgSingle import ArgSingle
from ........... import enums
from ........... import repcap

class MaximumCls:
    """Maximum commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('maximum', core, parent)

    def get(self, result: enums.SelectAll=None, carrierComponent=repcap.CarrierComponent.Default, frame=repcap.Frame.Default) -> float:
        """SCPI: FETCh[:CC<cc>][:ISRC][:FRAMe<fr>]:SUMMary:EVM:DS4K:MAXimum 

		Snippet: value: float = driver.applications.k14Xnr5G.fetch.cc.isrc.frame.summary.evm.ds4K.maximum.get(result = enums.SelectAll.ALL, carrierComponent = repcap.CarrierComponent.Default, frame = repcap.Frame.Default) 

		No command help available 

			:param result: No help available
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param frame: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:return: evm: No help available"""
        param = ArgSingleList().compose_cmd_string(ArgSingle('result', result, DataType.Enum, enums.SelectAll, is_optional=True))
        carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
        frame_cmd_val = self._cmd_group.get_repcap_cmd_value(frame, repcap.Frame)
        response = self._core.io.query_str(f'FETCh:CC{carrierComponent_cmd_val}:ISRC:FRAMe{frame_cmd_val}:SUMMary:EVM:DS4K:MAXimum? {param}'.rstrip())
        return Conversions.str_to_float(response)