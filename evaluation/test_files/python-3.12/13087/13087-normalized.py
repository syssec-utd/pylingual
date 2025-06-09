def _post_resource(self, url, body):
    """
        Canvas POST method.
        """
    params = {}
    self._set_as_user(params)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Connection': 'keep-alive'}
    url = url + self._params(params)
    response = DAO.postURL(url, headers, json.dumps(body))
    if not (response.status == 200 or response.status == 204):
        raise DataFailureException(url, response.status, response.data)
    return json.loads(response.data)