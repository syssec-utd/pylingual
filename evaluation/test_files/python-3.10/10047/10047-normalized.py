def basic_auth_header(username, password):
    """generate a base64 encoded header to ask for a token. This means
                base64 encoding a username and password and adding to the
                Authorization header to identify the client.

    Parameters
    ==========
    username: the username
    password: the password
   
    """
    s = '%s:%s' % (username, password)
    if sys.version_info[0] >= 3:
        s = bytes(s, 'utf-8')
        credentials = base64.b64encode(s).decode('utf-8')
    else:
        credentials = base64.b64encode(s)
    auth = {'Authorization': 'Basic %s' % credentials}
    return auth