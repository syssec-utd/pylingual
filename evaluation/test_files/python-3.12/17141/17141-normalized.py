def select_renderer(request: web.Request, renderers: OrderedDict, force=True):
    """
    Given a request, a list of renderers, and the ``force`` configuration
    option, return a two-tuple of:
    (media type, render callable). Uses mimeparse to find the best media
    type match from the ACCEPT header.
    """
    header = request.headers.get('ACCEPT', '*/*')
    best_match = mimeparse.best_match(renderers.keys(), header)
    if not best_match or best_match not in renderers:
        if force:
            return tuple(renderers.items())[0]
        else:
            raise web.HTTPNotAcceptable
    return (best_match, renderers[best_match])