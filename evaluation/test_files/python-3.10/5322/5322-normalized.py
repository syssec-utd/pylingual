def s3_keys_from_s3cfg(opt):
    """Retrieve S3 access key settings from s3cmd's config file, if present; otherwise return None."""
    try:
        if opt.s3cfg != None:
            s3cfg_path = '%s' % opt.s3cfg
        else:
            s3cfg_path = '%s/.s3cfg' % os.environ['HOME']
        if not os.path.exists(s3cfg_path):
            return None
        config = ConfigParser.ConfigParser()
        config.read(s3cfg_path)
        keys = (config.get('default', 'access_key'), config.get('default', 'secret_key'))
        debug('read S3 keys from %s file', s3cfg_path)
        return keys
    except Exception as e:
        info('could not read S3 keys from %s file; skipping (%s)', s3cfg_path, e)
        return None