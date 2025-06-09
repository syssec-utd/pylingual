def auth(self, skypeToken):
    """
        Request a new registration token using a current Skype token.

        Args:
            skypeToken (str): existing Skype token

        Returns:
            (str, datetime.datetime, str, SkypeEndpoint) tuple: registration token, associated expiry if known,
                                                                resulting endpoint hostname, endpoint if provided

        Raises:
            .SkypeAuthException: if the login request is rejected
            .SkypeApiException: if the login form can't be processed
        """
    token = expiry = endpoint = None
    msgsHost = SkypeConnection.API_MSGSHOST
    while not token:
        secs = int(time.time())
        hash = self.getMac256Hash(str(secs))
        headers = {'LockAndKey': 'appId=msmsgs@msnmsgr.com; time={0}; lockAndKeyResponse={1}'.format(secs, hash), 'Authentication': 'skypetoken=' + skypeToken, 'BehaviorOverride': 'redirectAs404'}
        endpointResp = self.conn('POST', '{0}/users/ME/endpoints'.format(msgsHost), codes=(200, 201, 404), headers=headers, json={'endpointFeatures': 'Agent'})
        regTokenHead = endpointResp.headers.get('Set-RegistrationToken')
        locHead = endpointResp.headers.get('Location')
        if locHead:
            locParts = re.search('(https://[^/]+/v1)/users/ME/endpoints(/(%7B[a-z0-9\\-]+%7D))?', locHead).groups()
            if locParts[2]:
                endpoint = SkypeEndpoint(self.conn, locParts[2].replace('%7B', '{').replace('%7D', '}'))
            if not locParts[0] == msgsHost:
                msgsHost = locHead.rsplit('/', 4 if locParts[2] else 3)[0]
                continue
        if regTokenHead:
            token = re.search('(registrationToken=[a-z0-9\\+/=]+)', regTokenHead, re.I).group(1)
            regExpiry = re.search('expires=(\\d+)', regTokenHead).group(1)
            expiry = datetime.fromtimestamp(int(regExpiry))
            regEndMatch = re.search('endpointId=({[a-z0-9\\-]+})', regTokenHead)
            if regEndMatch:
                endpoint = SkypeEndpoint(self.conn, regEndMatch.group(1))
        if not endpoint and endpointResp.status_code == 200 and endpointResp.json():
            endpoint = SkypeEndpoint(self.conn, endpointResp.json()[0]['id'])
    return (token, expiry, msgsHost, endpoint)