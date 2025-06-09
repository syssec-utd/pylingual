def unprotect_response(self, response, **kwargs):
    """
        Removes protection from the specified response
        :param request: response from the key vault service
        :return: unprotected response with any security protocal encryption removed
        """
    body = response.content
    if not self.supports_protection() or len(response.content) == 0 or response.status_code != 200:
        return response
    if 'application/jose+json' not in response.headers.get('content-type', '').lower():
        raise ValueError('Invalid protected response')
    jws = _JwsObject().deserialize(body)
    jws_header = _JwsHeader.from_compact_header(jws.protected)
    if jws_header.kid != self.server_signature_key.kid or jws_header.alg != 'RS256':
        raise ValueError('Invalid protected response')
    data = (jws.protected + '.' + jws.payload).encode('ascii')
    self.server_signature_key.verify(signature=_b64_to_bstr(jws.signature), data=data)
    decrypted = self._unprotect_payload(jws.payload)
    response._content = decrypted
    response.headers['Content-Type'] = 'application/json'
    return response