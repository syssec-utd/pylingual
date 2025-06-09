async def resume(self, *, device: Optional[SomeDevice]=None):
    """Resume playback on the user's account.

        Parameters
        ----------
        device : Optional[:obj:`SomeDevice`]
            The Device object or id of the device this command is targeting.
            If not supplied, the user’s currently active device is the target.
        """
    await self._user.http.play_playback(None, device_id=str(device))