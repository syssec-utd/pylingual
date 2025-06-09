from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap

class ChannelCls:
    """Channel commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Ch1"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('channel', core, parent)
        self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Ch1)

    def repcap_channel_set(self, channel: repcap.Channel) -> None:
        """Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Ch1"""
        self._cmd_group.set_repcap_enum_value(channel)

    def repcap_channel_get(self) -> repcap.Channel:
        """Returns the current default repeated capability for the child set/get methods"""
        return self._cmd_group.get_repcap_enum_value()

    def set(self, name: str, subBlock=repcap.SubBlock.Default, channel=repcap.Channel.Default) -> None:
        """SCPI: [SENSe]:POWer:ACHannel:SBLock<sb>:NAME[:CHANnel<ch>] 

		Snippet: driver.sense.power.achannel.sblock.name.channel.set(name = '1', subBlock = repcap.SubBlock.Default, channel = repcap.Channel.Default) 

		This command defines the name of the specified MSR Tx channel. This command is for MSR signals only.
		In MSR ACLR measurements, the default TX channel names correspond to the specified technology, followed by a consecutive
		number. The assigned sub block (A,B,C,D,E,F,G,H) is indicated as a prefix (e.g. A: WCDMA1) . This command is for MSR
		signals only (see method RsFsw.Calculate.Marker.Function.Power.preset) . For details on MSR signals see 'Measurement on
		multi-standard radio (MSR) signals'. 

			:param name: String containing the name of the channel
			:param subBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sblock')
			:param channel: optional repeated capability selector. Default value: Ch1 (settable in the interface 'Channel')
		"""
        param = Conversions.value_to_quoted_str(name)
        subBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(subBlock, repcap.SubBlock)
        channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
        self._core.io.write(f'SENSe:POWer:ACHannel:SBLock{subBlock_cmd_val}:NAME:CHANnel{channel_cmd_val} {param}')

    def get(self, subBlock=repcap.SubBlock.Default, channel=repcap.Channel.Default) -> str:
        """SCPI: [SENSe]:POWer:ACHannel:SBLock<sb>:NAME[:CHANnel<ch>] 

		Snippet: value: str = driver.sense.power.achannel.sblock.name.channel.get(subBlock = repcap.SubBlock.Default, channel = repcap.Channel.Default) 

		This command defines the name of the specified MSR Tx channel. This command is for MSR signals only.
		In MSR ACLR measurements, the default TX channel names correspond to the specified technology, followed by a consecutive
		number. The assigned sub block (A,B,C,D,E,F,G,H) is indicated as a prefix (e.g. A: WCDMA1) . This command is for MSR
		signals only (see method RsFsw.Calculate.Marker.Function.Power.preset) . For details on MSR signals see 'Measurement on
		multi-standard radio (MSR) signals'. 

			:param subBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sblock')
			:param channel: optional repeated capability selector. Default value: Ch1 (settable in the interface 'Channel')
			:return: name: String containing the name of the channel"""
        subBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(subBlock, repcap.SubBlock)
        channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
        response = self._core.io.query_str(f'SENSe:POWer:ACHannel:SBLock{subBlock_cmd_val}:NAME:CHANnel{channel_cmd_val}?')
        return trim_str_response(response)

    def clone(self) -> 'ChannelCls':
        """Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
        new_group = ChannelCls(self._core, self._cmd_group.parent)
        self._cmd_group.synchronize_repcaps(new_group)
        return new_group