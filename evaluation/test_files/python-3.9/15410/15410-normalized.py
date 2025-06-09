def extra_data(self):
    """Load token data stored in token (ignores expiry date of tokens)."""
    if self.token:
        return SecretLinkFactory.load_token(self.token, force=True)['data']
    return None