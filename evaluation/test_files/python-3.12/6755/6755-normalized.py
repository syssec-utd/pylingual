def _request(self, method, url, **kwargs):
    """Make HTTP request and return response object

            Args:
                method (str): GET, POST, PUT, DELETE
                url (str): path appended to the base_url to create request
                **kwargs: passed directly to a requests.request object
        """
    resp = self._session.request(method, '{}/{}'.format(self._base_url, url), headers=self._headers, **kwargs)
    try:
        resp.raise_for_status()
    except HTTPError as e:
        logging.error(resp.content)
        raise RestClientError(e)
    return resp