def _request(self, req_type, url, **kwargs):
    """
        Make a request via the `requests` module. If the result has an HTTP
        error status, convert that to a Python exception.
        """
    logger.debug('%s %s' % (req_type, url))
    result = self.session.request(req_type, url, **kwargs)
    try:
        result.raise_for_status()
    except requests.HTTPError:
        error = result.text
        try:
            error = json.loads(error)
        except ValueError:
            pass
        if result.status_code in (401, 403):
            error_class = LuminosoAuthError
        elif result.status_code in (400, 404, 405):
            error_class = LuminosoClientError
        elif result.status_code >= 500:
            error_class = LuminosoServerError
        else:
            error_class = LuminosoError
        raise error_class(error)
    return result