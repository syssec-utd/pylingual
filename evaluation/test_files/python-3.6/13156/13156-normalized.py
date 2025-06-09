def call_api(self, method, url, headers=None, params=None, data=None, files=None, timeout=None):
    """ Call API.

        This returns object containing data, with error details if applicable.

        Args:
            method (str): The HTTP method to use.
            url (str): Resource location relative to the base URL.
            headers (dict or None): Extra request headers to set.
            params (dict or None): Query-string parameters.
            data (dict or None): Request body contents for POST or PUT requests.
            files (dict or None: Files to be passed to the request.
            timeout (int): Maximum time before timing out.

        Returns:
            ResultParser or ErrorParser.
        """
    method = method.upper()
    headers = deepcopy(headers) or {}
    headers['Accept'] = self.accept_type
    params = deepcopy(params) or {}
    data = data or {}
    files = files or {}
    if self.username and self.api_key:
        params.update(self.get_credentials())
    url = urljoin(self.base_url, url)
    r = requests.request(method, url, headers=headers, params=params, files=files, data=data, timeout=timeout)
    return (r, r.status_code)