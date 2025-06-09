def _api_post(self, url, **kwargs):
    """
        Convenience method for posting
        """
    response = self.session.post(url=url, headers=self._get_api_headers(), **kwargs)
    if not response.ok:
        raise ServerException('{0}: {1}'.format(response.status_code, response.text or response.reason))
    return response.json()