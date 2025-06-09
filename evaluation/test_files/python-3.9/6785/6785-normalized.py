async def reorder_tracks(self, playlist, start, insert_before, length=1, *, snapshot_id=None):
    """Reorder a track or a group of tracks in a playlist.

        Parameters
        ----------
        playlist : Union[str, Playlist]
            The playlist to modify
        start : int
            The position of the first track to be reordered.
        insert_before : int
            The position where the tracks should be inserted.
        length : Optional[int]
            The amount of tracks to be reordered. Defaults to 1 if not set.
        snapshot_id : str
            The playlist’s snapshot ID against which you want to make the changes.

        Returns
        -------
        snapshot_id : str
            The snapshot id of the playlist.
        """
    data = await self.http.reorder_playlists_tracks(self.id, str(playlist), start, length, insert_before, snapshot_id=snapshot_id)
    return data['snapshot_id']