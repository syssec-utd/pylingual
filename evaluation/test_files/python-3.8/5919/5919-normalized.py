def _make_client_with_token(self, token):
    """Uses cached client or create new one with specific token."""
    cached_clients = getattr(self, 'clients', None)
    hashed_token = _hash_token(self, token)
    if cached_clients and hashed_token in cached_clients:
        return cached_clients[hashed_token]
    client = self.make_client(token)
    if cached_clients:
        cached_clients[hashed_token] = client
    return client