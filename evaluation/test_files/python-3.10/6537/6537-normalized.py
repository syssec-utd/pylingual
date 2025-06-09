def execute(self, root_allowed=False):
    """Execute using self.data

        :param bool root_allowed: Only used for ExecuteCmd
        :return:
        """
    kwargs = {'stream': True, 'timeout': 15, 'headers': self.data.get('headers', {})}
    if self.data.get('content-type'):
        kwargs['headers']['content-type'] = self.data['content-type']
    if self.data.get('body'):
        kwargs['data'] = self.data['body']
    if self.data.get('auth'):
        kwargs['auth'] = tuple(self.data['auth'].split(':', 1))
    try:
        resp = request(self.data.get('method', 'get').lower(), self.data['url'], verify=self.data.get('verify', True), **kwargs)
    except RequestException as e:
        raise ExecuteError('Exception on request to {}: {}'.format(self.data['url'], e))
    if resp.status_code >= 400:
        raise ExecuteError('"{}" return code {}.'.format(self.data['url'], resp.status_code))
    data = resp.raw.read(1000, decode_content=True)
    if sys.version_info >= (3,):
        data = data.decode('utf-8', errors='ignore')
    return data