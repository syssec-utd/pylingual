from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap

class StateCls:
    """State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('state', core, parent)

    def set(self, state: bool, inputIx=repcap.InputIx.Default) -> None:
        """SCPI: INPut<Undef>:EATT:STATe 

		Snippet: driver.applications.k17Mcgd.inputPy.eatt.state.set(state = False, inputIx = repcap.InputIx.Default) 

		This command turns the electronic attenuator on and off. 

			:param state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on
			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InputPy')
		"""
        param = Conversions.bool_to_str(state)
        inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
        self._core.io.write(f'INPut{inputIx_cmd_val}:EATT:STATe {param}')

    def get(self, inputIx=repcap.InputIx.Default) -> bool:
        """SCPI: INPut<Undef>:EATT:STATe 

		Snippet: value: bool = driver.applications.k17Mcgd.inputPy.eatt.state.get(inputIx = repcap.InputIx.Default) 

		This command turns the electronic attenuator on and off. 

			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InputPy')
			:return: state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on"""
        inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
        response = self._core.io.query_str(f'INPut{inputIx_cmd_val}:EATT:STATe?')
        return Conversions.str_to_bool(response)