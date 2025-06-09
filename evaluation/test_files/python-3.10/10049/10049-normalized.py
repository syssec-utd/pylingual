def generate_credential(s):
    """basic_auth_header will return a base64 encoded header object to
    :param username: the username
    """
    if sys.version_info[0] >= 3:
        s = bytes(s, 'utf-8')
        credentials = base64.b64encode(s).decode('utf-8')
    else:
        credentials = base64.b64encode(s)
    return credentials