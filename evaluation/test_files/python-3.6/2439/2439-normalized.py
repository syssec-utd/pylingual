def get_authorization_server(self):
    """ Returns the URI for the authorization server if present, otherwise empty string. """
    value = ''
    for key in ['authorization_uri', 'authorization']:
        value = self.get_value(key) or ''
        if value:
            break
    return value