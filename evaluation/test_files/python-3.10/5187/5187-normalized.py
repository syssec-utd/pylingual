def sanitize_for_archive(url, headers, payload):
    """Sanitize payload of a HTTP request by removing the token information
        before storing/retrieving archived items

        :param: url: HTTP url request
        :param: headers: HTTP headers request
        :param: payload: HTTP payload request

        :returns url, headers and the sanitized payload
        """
    if '__conduit__' in payload['params']:
        params = json.loads(payload['params'])
        params.pop('__conduit__')
        payload['params'] = json.dumps(params, sort_keys=True)
    return (url, headers, payload)