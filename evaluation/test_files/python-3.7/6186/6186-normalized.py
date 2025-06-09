def _getter(self, url, subkey=None):
    """ Pagination utility.  Obnoxious. """
    kwargs = {}
    if 'basic' in self.auth:
        kwargs['auth'] = self.auth['basic']
    results = []
    link = dict(next=url)
    while 'next' in link:
        response = self.session.get(link['next'], **kwargs)
        if response.status_code == 404 and 'token' in self.auth:
            log.warn("A '404' from github may indicate an auth failure. Make sure both that your token is correct and that it has 'public_repo' and not 'public access' rights.")
        json_res = self.json_response(response)
        if subkey is not None:
            json_res = json_res[subkey]
        results += json_res
        link = self._link_field_to_dict(response.headers.get('link', None))
    return results