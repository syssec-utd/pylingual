def get_endpoints(self, query=None):
    """use a transfer client to get endpoints. If a search term is included,
       we use it to search a scope of "all" in addition to personal and shared
       endpoints. Endpoints are organized
       by type (my-endpoints, shared-with-me, optionally all) and then id.

       Parameters
       ==========
       query: an endpoint search term to add to a scope "all" search. If not 
              defined, no searches are done with "all"

    """
    self.endpoints = {}
    if not hasattr(self, 'transfer_client'):
        self._init_transfer_client()
    scopes = {'my-endpoints': None, 'shared-with-me': None}
    if query is not None:
        scopes.update({'all': query})
    for scope, q in scopes.items():
        self.endpoints[scope] = {}
        for ep in self.transfer_client.endpoint_search(q, filter_scope=scope):
            ep = ep.__dict__['_data']
            self.endpoints[scope][ep['id']] = ep
    if len(self.endpoints['my-endpoints']) == 0:
        bot.warning('No personal endpoint found for local transfer.')
        bot.warning('https://www.globus.org/globus-connect-personal')
    return self.endpoints