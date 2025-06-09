def validate_token(cls, token, expected_data):
    """Validate a secret link token.

        Only queries the database if token is valid to determine that the token
        has not been revoked.
        """
    data = SecretLinkFactory.validate_token(token, expected_data=expected_data)
    if data:
        link = cls.query.get(data['id'])
        if link and link.is_valid():
            return True
    return False