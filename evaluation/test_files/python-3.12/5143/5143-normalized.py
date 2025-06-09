def get_recent_pages(self, namespaces, rccontinue=''):
    """Retrieve recent pages from all namespaces starting from rccontinue."""
    namespaces.sort()
    params = {'action': 'query', 'list': 'recentchanges', 'rclimit': self.limit, 'rcnamespace': '|'.join(namespaces), 'rcprop': 'title|timestamp|ids', 'format': 'json'}
    if rccontinue:
        params['rccontinue'] = rccontinue
    return self.call(params)