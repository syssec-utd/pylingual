async def get_tracks(self, *, limit=20, offset=0) -> List[Track]:
    """Get a list of the songs saved in the current Spotify user’s ‘Your Music’ library.

        Parameters
        ----------
        limit : Optional[int]
            The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
        offset : Optional[int]
            The index of the first item to return. Default: 0
        """
    data = await self.user.http.saved_tracks(limit=limit, offset=offset)
    return [Track(self.__client, item['track']) for item in data['items']]