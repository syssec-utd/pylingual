def _x_credentials_parser(credentials, data):
    """
        We need to override this method to fix Facebooks naming deviation.
        """
    credentials.expire_in = data.get('expires')
    if data.get('token_type') == 'bearer':
        credentials.token_type = 'Bearer'
    return credentials