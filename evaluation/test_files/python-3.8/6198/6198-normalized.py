def get_service_password(service, username, oracle=None, interactive=False):
    """
    Retrieve the sensitive password for a service by:

      * retrieving password from a secure store (@oracle:use_keyring, default)
      * asking the password from the user (@oracle:ask_password, interactive)
      * executing a command and use the output as password
        (@oracle:eval:<command>)

    Note that the keyring may or may not be locked
    which requires that the user provides a password (interactive mode).

    :param service:     Service name, may be key into secure store (as string).
    :param username:    Username for the service (as string).
    :param oracle:      Hint which password oracle strategy to use.
    :return: Retrieved password (as string)

    .. seealso::
        https://bitbucket.org/kang/python-keyring-lib
    """
    import getpass
    password = None
    if not oracle or oracle == '@oracle:use_keyring':
        keyring = get_keyring()
        password = keyring.get_password(service, username)
        if interactive and password is None:
            oracle = '@oracle:ask_password'
            password = get_service_password(service, username, oracle, interactive=True)
            if password:
                keyring.set_password(service, username, password)
    elif interactive and oracle == '@oracle:ask_password':
        prompt = '%s password: ' % service
        password = getpass.getpass(prompt)
    elif oracle.startswith('@oracle:eval:'):
        command = oracle[13:]
        return oracle_eval(command)
    if password is None:
        die("MISSING PASSWORD: oracle='%s', interactive=%s for service=%s" % (oracle, interactive, service))
    return password