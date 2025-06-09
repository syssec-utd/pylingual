from typing import Optional
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.current_relay_info import CurrentRelayInfo
from zepben.evolve.model.cim.iec61970.base.protection.protection_equipment import ProtectionEquipment
__all__ = ['CurrentRelay']

class CurrentRelay(ProtectionEquipment):
    """A device that checks current flow values in any direction or designated direction."""
    current_limit_1: Optional[float] = None
    'Current limit number 1 for inverse time pickup in amperes.'
    inverse_time_flag: Optional[bool] = None
    'Set true if the current relay has inverse time characteristic.'
    time_delay_1: Optional[float] = None
    'Inverse time delay number 1 for current limit number 1 in seconds.'

    @property
    def current_relay_info(self) -> Optional[CurrentRelayInfo]:
        """Datasheet information for this :class:`CurrentRelay`."""
        return self.asset_info

    @current_relay_info.setter
    def current_relay_info(self, cri: Optional[CurrentRelayInfo]):
        """
        Set the :class:`CurrentRelayInfo` for this :class:`CurrentRelay`
        :param cri: The CurrentRelayInfo for this CurrentRelay
        """
        self.asset_info = cri