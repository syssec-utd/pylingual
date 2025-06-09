def send(self, encoding='json'):
    """Send the message via HTTP POST, default is json-encoded."""
    self._construct_message()
    if self.verbose:
        print('Debugging info\n--------------\n{} Message created.'.format(timestamp()))
    if encoding == 'json':
        resp = requests.post(self.url, json=self.message)
    elif encoding == 'url':
        resp = requests.post(self.url, data=self.message)
    try:
        resp.raise_for_status()
        if resp.history and resp.history[0].status_code >= 300:
            raise MessageSendError('HTTP Redirect: Possibly Invalid authentication')
        elif 'invalid_auth' in resp.text:
            raise MessageSendError('Invalid Auth: Possibly Bad Auth Token')
    except (requests.exceptions.HTTPError, MessageSendError) as e:
        raise MessageSendError(e)
    if self.verbose:
        print(timestamp(), type(self).__name__, ' info:', self.__str__(indentation='\n * '), '\n * HTTP status code:', resp.status_code)
    print('Message sent.')