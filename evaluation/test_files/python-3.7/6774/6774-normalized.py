async def get_all_albums(self, *, market='US') -> List[Album]:
    """loads all of the artists albums, depending on how many the artist has this may be a long operation.

        Parameters
        ----------
        market : Optional[str]
            An ISO 3166-1 alpha-2 country code.

        Returns
        -------
        albums : List[Album]
            The albums of the artist.
        """
    from .album import Album
    albums = []
    offset = 0
    total = await self.total_albums(market=market)
    while len(albums) < total:
        data = await self.__client.http.artist_albums(self.id, limit=50, offset=offset, market=market)
        offset += 50
        albums += list((Album(self.__client, item) for item in data['items']))
    return albums