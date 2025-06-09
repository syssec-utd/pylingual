def _fetch(self, endpoint_name, **params):
    """
        Wrapper for making an api request from giphy
        """
    params['api_key'] = self.api_key
    resp = requests.get(self._endpoint(endpoint_name), params=params)
    resp.raise_for_status()
    data = resp.json()
    self._check_or_raise(data.get('meta', {}))
    return data