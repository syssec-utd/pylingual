def write_auth(msg_type, profile_name, auth, cfg):
    """
    Write the settings into the auth portion of the cfg.

    Args:
        :msg_type: (str) message type to create config entry.
        :profile_name: (str) name of the profile entry
        :auth: (dict) auth parameters
        :cfg: (jsonconfig.Config) config instance.
    """
    key_fmt = profile_name + '_' + msg_type
    pwd = []
    for k, v in CONFIG[msg_type]['auth'].items():
        pwd.append(auth[k])
    if len(pwd) > 1:
        cfg.pwd[key_fmt] = ' :: '.join(pwd)
    else:
        cfg.pwd[key_fmt] = pwd[0]