def save_notebook(self, notebook_id, data, name=None, format=u'json'):
    """Save an existing notebook by notebook_id."""
    if format not in self.allowed_formats:
        raise web.HTTPError(415, u'Invalid notebook format: %s' % format)
    try:
        nb = current.reads(data.decode('utf-8'), format)
    except:
        raise web.HTTPError(400, u'Invalid JSON data')
    if name is not None:
        nb.metadata.name = name
    self.save_notebook_object(notebook_id, nb)