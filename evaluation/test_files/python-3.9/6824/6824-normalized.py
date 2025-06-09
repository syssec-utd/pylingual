async def transfer(self, device: SomeDevice, ensure_playback: bool=False):
    """Transfer playback to a new device and determine if it should start playing.

        Parameters
        ----------
        device : :obj:`SomeDevice`
            The device on which playback should be started/transferred.
        ensure_playback : bool
            if `True` ensure playback happens on new device.
            else keep the current playback state.
        """
    await self._user.http.transfer_player(str(device), play=ensure_playback)