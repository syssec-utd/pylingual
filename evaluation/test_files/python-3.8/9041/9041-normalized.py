def get_root_url(url, warn=True):
    """
    Get the "root URL" for a URL, as described in the LuminosoClient
    documentation.
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        raise ValueError('Please supply a full URL, beginning with http:// or https:// .')
    root_url = '%s://%s/api/v4' % (parsed_url.scheme, parsed_url.netloc)
    if warn and (not parsed_url.path.startswith('/api/v4')):
        logger.warning('Using %s as the root url' % root_url)
    return root_url