def login(self, ptrt_url):
    """
        Create session using BBC ID. See https://www.bbc.co.uk/usingthebbc/account/

        :param ptrt_url: The snapback URL to redirect to after successful authentication
        :type ptrt_url: string
        :return: Whether authentication was successful
        :rtype: bool
        """

    def auth_check(res):
        return ptrt_url in [h.url for h in res.history] + [res.url]
    session_res = self.session.http.get(self.session_url, params=dict(ptrt=ptrt_url))
    if auth_check(session_res):
        log.debug('Already authenticated, skipping authentication')
        return True
    http_nonce = self._extract_nonce(session_res)
    res = self.session.http.post(self.auth_url, params=dict(ptrt=ptrt_url, nonce=http_nonce), data=dict(jsEnabled=True, username=self.get_option('username'), password=self.get_option('password'), attempts=0), headers={'Referer': self.url})
    return auth_check(res)