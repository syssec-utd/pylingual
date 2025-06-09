def build(self, secret_key):
    """Builds a final copy of the token using the given secret key.

        :param secret_key(string): The secret key that corresponds to this builder's access key.
        """
    key = jwk.JWK(kty='oct', k=base64url_encode(uuid.UUID(secret_key).bytes))
    header = {'alg': 'dir', 'enc': 'A128GCM', 'zip': 'DEF', 'cty': 'JWT', 'kid': self._access_key}
    now = int(time.time())
    payload = {'iat': now, 'nbf': now}
    if self._expiration is not None:
        payload['exp'] = int(calendar.timegm(self._expiration.utctimetuple()))
    if len(self._view_identifiers) > 0:
        payload[VIEW_IDENTIFIERS_CLAIM_NAME] = self._view_identifiers
    if len(self._parameters) > 0:
        parameters = []
        for parameter in self._parameters:
            serialized = {'field': parameter.field, 'op': parameter.op}
            if hasattr(parameter, '__iter__'):
                serialized['any'] = list(parameter.value)
            else:
                serialized['value'] = parameter.value
            parameters.append(serialized)
        payload[PARAMETERS_CLAIM_NAME] = parameters
    if len(self._attributes) > 0:
        payload[ATTRIBUTES_CLAIM_NAME] = self._attributes
    tok = jwe.JWE(json_encode(payload), protected=header)
    tok.add_recipient(key)
    return tok.serialize(compact=True)