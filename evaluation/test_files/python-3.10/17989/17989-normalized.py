def get_image_size(self, token, resolution=0):
    """
        Return the size of the volume (3D). Convenient for when you want
        to download the entirety of a dataset.

        Arguments:
            token (str): The token for which to find the dataset image bounds
            resolution (int : 0): The resolution at which to get image bounds.
                Defaults to 0, to get the largest area available.

        Returns:
            int[3]: The size of the bounds. Should == get_volume.shape

        Raises:
            RemoteDataNotFoundError: If the token is invalid, or if the
                metadata at that resolution is unavailable in projinfo.
        """
    info = self.get_proj_info(token)
    res = str(resolution)
    if res not in info['dataset']['imagesize']:
        raise RemoteDataNotFoundError('Resolution ' + res + ' is not available.')
    return info['dataset']['imagesize'][str(resolution)]