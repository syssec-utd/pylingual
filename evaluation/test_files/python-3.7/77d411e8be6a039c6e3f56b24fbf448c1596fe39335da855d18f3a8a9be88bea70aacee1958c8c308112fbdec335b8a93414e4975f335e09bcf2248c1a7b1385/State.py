from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap

class StateCls:
    """State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('state', core, parent)

    def set(self, state: bool, window=repcap.Window.Default, limitIx=repcap.LimitIx.Default, gapChannel=repcap.GapChannel.Default) -> None:
        """SCPI: CALCulate<n>:LIMit<li>:ACPower:GAP<gap>[:AUTO][:CACLr][:RELative]:STATe 

		Snippet: driver.calculate.limit.acPower.gap.auto.caclr.relative.state.set(state = False, window = repcap.Window.Default, limitIx = repcap.LimitIx.Default, gapChannel = repcap.GapChannel.Default) 

		This command turns the relative limit check for the specified gap (CACLR) channel on and off. You have to activate the
		general ACLR limit check before using this command with method RsFsw.Calculate.Limit.AcPower.State.set. 

			:param state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:param limitIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Limit')
			:param gapChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gap')
		"""
        param = Conversions.bool_to_str(state)
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        limitIx_cmd_val = self._cmd_group.get_repcap_cmd_value(limitIx, repcap.LimitIx)
        gapChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(gapChannel, repcap.GapChannel)
        self._core.io.write(f'CALCulate{window_cmd_val}:LIMit{limitIx_cmd_val}:ACPower:GAP{gapChannel_cmd_val}:AUTO:CACLr:RELative:STATe {param}')

    def get(self, window=repcap.Window.Default, limitIx=repcap.LimitIx.Default, gapChannel=repcap.GapChannel.Default) -> bool:
        """SCPI: CALCulate<n>:LIMit<li>:ACPower:GAP<gap>[:AUTO][:CACLr][:RELative]:STATe 

		Snippet: value: bool = driver.calculate.limit.acPower.gap.auto.caclr.relative.state.get(window = repcap.Window.Default, limitIx = repcap.LimitIx.Default, gapChannel = repcap.GapChannel.Default) 

		This command turns the relative limit check for the specified gap (CACLR) channel on and off. You have to activate the
		general ACLR limit check before using this command with method RsFsw.Calculate.Limit.AcPower.State.set. 

			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:param limitIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Limit')
			:param gapChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gap')
			:return: state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on"""
        window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
        limitIx_cmd_val = self._cmd_group.get_repcap_cmd_value(limitIx, repcap.LimitIx)
        gapChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(gapChannel, repcap.GapChannel)
        response = self._core.io.query_str(f'CALCulate{window_cmd_val}:LIMit{limitIx_cmd_val}:ACPower:GAP{gapChannel_cmd_val}:AUTO:CACLr:RELative:STATe?')
        return Conversions.str_to_bool(response)