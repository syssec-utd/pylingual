def _parse_s3_config(config_file_name, config_format='boto', profile=None):
    """
    Parses a config file for s3 credentials. Can currently
    parse boto, s3cmd.conf and AWS SDK config formats

    :param config_file_name: path to the config file
    :type config_file_name: str
    :param config_format: config type. One of "boto", "s3cmd" or "aws".
        Defaults to "boto"
    :type config_format: str
    :param profile: profile name in AWS type config file
    :type profile: str
    """
    config = configparser.ConfigParser()
    if config.read(config_file_name):
        sections = config.sections()
    else:
        raise AirflowException("Couldn't read {0}".format(config_file_name))
    if config_format is None:
        config_format = 'boto'
    conf_format = config_format.lower()
    if conf_format == 'boto':
        if profile is not None and 'profile ' + profile in sections:
            cred_section = 'profile ' + profile
        else:
            cred_section = 'Credentials'
    elif conf_format == 'aws' and profile is not None:
        cred_section = profile
    else:
        cred_section = 'default'
    if conf_format in ('boto', 'aws'):
        key_id_option = 'aws_access_key_id'
        secret_key_option = 'aws_secret_access_key'
    else:
        key_id_option = 'access_key'
        secret_key_option = 'secret_key'
    if cred_section not in sections:
        raise AirflowException('This config file format is not recognized')
    else:
        try:
            access_key = config.get(cred_section, key_id_option)
            secret_key = config.get(cred_section, secret_key_option)
        except Exception:
            logging.warning('Option Error in parsing s3 config file')
            raise
        return (access_key, secret_key)