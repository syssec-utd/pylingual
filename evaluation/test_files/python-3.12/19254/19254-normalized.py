def api_doc(full_version, resource, method='GET', **kwargs):
    """
    >>> # Wrap api endpoints with more details
    >>> api_doc('/resource', secure=True, key='value')
    GET /resource?secure=true&key=value
    """
    doc = '{} {}'.format(method, api_url(full_version, resource))
    params = '&'.join(['{}={}'.format(k, v) for k, v in kwargs.iteritems()])
    if params:
        doc = '?'.join([doc, params])
    return doc