def _api_call(self, entrypoint, params=None, schema=None):
    """Makes a call against the api.

        :param entrypoint: API method to call.
        :param params: parameters to include in the request data.
        :param schema: schema to use to validate the data
        """
    url = self._api_url.format(entrypoint)
    params = params or {}
    if self.session_id:
        params.update({'session_id': self.session_id})
    else:
        params.update({'device_id': self.device_id, 'device_type': self._access_type, 'access_token': self._access_token, 'version': self._version_code})
    params.update({'locale': self.locale.replace('_', '')})
    if self.session_id:
        params['session_id'] = self.session_id
    res = self.session.http.post(url, data=params, headers=self.headers, verify=False)
    json_res = self.session.http.json(res, schema=_api_schema)
    if json_res['error']:
        err_msg = json_res.get('message', 'Unknown error')
        err_code = json_res.get('code', 'unknown_error')
        raise CrunchyrollAPIError(err_msg, err_code)
    data = json_res.get('data')
    if schema:
        data = schema.validate(data, name='API response')
    return data