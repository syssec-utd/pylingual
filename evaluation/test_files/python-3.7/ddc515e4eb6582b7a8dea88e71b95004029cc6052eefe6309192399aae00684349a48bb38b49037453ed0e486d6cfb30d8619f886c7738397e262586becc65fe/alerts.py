"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
from teslajsonpy.homeassistant.vehicle import VehicleDevice

class Horn(VehicleDevice):
    """Home-Assistant class for horn of Tesla vehicles."""

    def __init__(self, data, controller):
        """Initialize the horn for the vehicle.

        Parameters
        ----------
        data : dict
            The horn for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/commands/alerts
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.type = 'horn'
        self.hass_type = 'button'
        self.name = self._name()
        self.uniq_name = self._uniq_name()

    async def async_update(self, wake_if_asleep=False, force=False):
        """Update the horn of the vehicle."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    async def honk_horn(self) -> None:
        """Horn."""
        await self._controller.api('HONK_HORN', path_vars={'vehicle_id': self._id}, on=True, wake_if_asleep=True)

class FlashLights(VehicleDevice):
    """Home-Assistant class for flash lights of Tesla vehicles."""

    def __init__(self, data, controller):
        """Initialize the flash lights for the vehicle.

        Parameters
        ----------
        data : dict
            The flash lights for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/commands/alerts
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.type = 'flash lights'
        self.hass_type = 'button'
        self.name = self._name()
        self.uniq_name = self._uniq_name()

    async def async_update(self, wake_if_asleep=False, force=False):
        """Update the flash lights of the vehicle."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    async def flash_lights(self) -> None:
        """Flash Lights."""
        await self._controller.api('FLASH_LIGHTS', path_vars={'vehicle_id': self._id}, on=True, wake_if_asleep=True)