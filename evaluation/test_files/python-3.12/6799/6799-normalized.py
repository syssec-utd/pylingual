async def contains_albums(self, *albums: Sequence[Union[str, Album]]) -> List[bool]:
    """Check if one or more albums is already saved in the current Spotify user’s ‘Your Music’ library.

        Parameters
        ----------
        albums : Union[Album, str]
            A sequence of artist objects or spotify IDs
        """
    _albums = [obj if isinstance(obj, str) else obj.id for obj in albums]
    return await self.user.http.is_saved_album(_albums)