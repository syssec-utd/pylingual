def create(self, subject, displayName, issuerToken, expiration, secret):
    """Create a new guest issuer using the provided issuer token.

        This function returns a guest issuer with an api access token.

        Args:
            subject(basestring): Unique and public identifier
            displayName(basestring): Display Name of the guest user
            issuerToken(basestring): Issuer token from developer hub
            expiration(basestring): Expiration time as a unix timestamp
            secret(basestring): The secret used to sign your guest issuers

        Returns:
            GuestIssuerToken: A Guest Issuer with a valid access token.

        Raises:
            TypeError: If the parameter types are incorrect
            ApiError: If the webex teams cloud returns an error.
        """
    check_type(subject, basestring)
    check_type(displayName, basestring)
    check_type(issuerToken, basestring)
    check_type(expiration, basestring)
    check_type(secret, basestring)
    payload = {'sub': subject, 'name': displayName, 'iss': issuerToken, 'exp': expiration}
    key = base64.b64decode(secret)
    jwt_token = jwt.encode(payload, key, algorithm='HS256')
    url = self._session.base_url + API_ENDPOINT + '/' + 'login'
    headers = {'Authorization': 'Bearer ' + jwt_token.decode('utf-8')}
    response = requests.post(url, headers=headers)
    check_response_code(response, EXPECTED_RESPONSE_CODE['GET'])
    return self._object_factory(OBJECT_TYPE, response.json())