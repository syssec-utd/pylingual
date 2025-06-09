async def remove_albums(self, *albums):
    """Remove one or more albums from the current user’s ‘Your Music’ library.

        Parameters
        ----------
        albums : Sequence[Union[Album, str]]
            A sequence of artist objects or spotify IDs
        """
    _albums = [obj if isinstance(obj, str) else obj.id for obj in albums]
    await self.user.http.delete_saved_albums(','.join(_albums))