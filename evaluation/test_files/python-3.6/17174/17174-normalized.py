def gif(self, gif_id, strict=False):
    """
        Retrieves a specifc gif from giphy based on unique id

        :param gif_id: Unique giphy gif ID
        :type gif_id: string
        :param strict: Whether an exception should be raised when no results
        :type strict: boolean
        """
    resp = self._fetch(gif_id)
    if resp['data']:
        return GiphyImage(resp['data'])
    elif strict or self.strict:
        raise GiphyApiException("GIF with ID '%s' could not be found" % gif_id)