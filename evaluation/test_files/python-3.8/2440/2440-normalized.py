def _validate_request_uri(self, uri):
    """ Extracts the host authority from the given URI. """
    if not uri:
        raise ValueError('request_uri cannot be empty')
    uri = parse.urlparse(uri)
    if not uri.netloc:
        raise ValueError('request_uri must be an absolute URI')
    if uri.scheme.lower() not in ['http', 'https']:
        raise ValueError('request_uri must be HTTP or HTTPS')
    return uri.netloc