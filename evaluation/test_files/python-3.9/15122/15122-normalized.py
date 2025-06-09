def create(self, data, resource='data'):
    """Create an object of resource:

        * data
        * project
        * processor
        * trigger
        * template

        :param data: Object values
        :type data: dict
        :param resource: Resource name
        :type resource: string

        """
    if isinstance(data, dict):
        data = json.dumps(data)
    if not isinstance(data, str):
        raise ValueError(mgs='data must be dict, str or unicode')
    resource = resource.lower()
    if resource not in ('data', 'project', 'processor', 'trigger', 'template'):
        raise ValueError(mgs='resource must be data, project, processor, trigger or template')
    if resource == 'project':
        resource = 'case'
    url = urlparse.urljoin(self.url, '/api/v1/{}/'.format(resource))
    return requests.post(url, data=data, auth=self.auth, headers={'cache-control': 'no-cache', 'content-type': 'application/json', 'accept': 'application/json, text/plain, */*', 'referer': self.url})