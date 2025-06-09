def get_rsa_key(self, client_key, request):
    """Retrieves a previously stored client provided RSA key."""
    if not request.client:
        request.client = self._clientgetter(client_key=client_key)
    if hasattr(request.client, 'rsa_key'):
        return request.client.rsa_key
    return None