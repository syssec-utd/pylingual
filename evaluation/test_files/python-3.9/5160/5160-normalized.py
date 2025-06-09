def fetch(self, url, payload=None, headers=None, method=GET, stream=False, verify=True):
    """Fetch the data from a given URL.

        :param url: link to the resource
        :param payload: payload of the request
        :param headers: headers of the request
        :param method: type of request call (GET or POST)
        :param stream: defer downloading the response body until the response content is available
        :param verify: verifying the SSL certificate

        :returns a response object
        """
    if self.from_archive:
        response = self._fetch_from_archive(url, payload, headers)
    else:
        response = self._fetch_from_remote(url, payload, headers, method, stream, verify)
    return response