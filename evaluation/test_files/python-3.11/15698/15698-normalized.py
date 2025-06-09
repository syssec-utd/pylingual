def read(self, path, params=None):
    """Read the result at the given path (GET) from the CRUD API, using the optional params dictionary
        as url parameters."""
    return self.handleresult(self.r.get(urljoin(self.url + CRUD_PATH, path), params=params))