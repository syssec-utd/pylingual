def find_path(self, notebook_id):
    """Return a full path to a notebook given its notebook_id."""
    try:
        name = self.mapping[notebook_id]
    except KeyError:
        raise web.HTTPError(404, u'Notebook does not exist: %s' % notebook_id)
    return self.get_path_by_name(name)