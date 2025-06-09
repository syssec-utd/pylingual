def config_for_set(uset, app, defaults=None):
    """
    This is a helper function for `configure_uploads` that extracts the
    configuration for a single set.

    :param uset: The upload set.
    :param app: The app to load the configuration from.
    :param defaults: A dict with keys `url` and `dest` from the
                     `UPLOADS_DEFAULT_DEST` and `DEFAULT_UPLOADS_URL`
                     settings.
    """
    config = app.config
    prefix = 'UPLOADED_%s_' % uset.name.upper()
    using_defaults = False
    if defaults is None:
        defaults = dict(dest=None, url=None)
    allow_extns = tuple(config.get(prefix + 'ALLOW', ()))
    deny_extns = tuple(config.get(prefix + 'DENY', ()))
    destination = config.get(prefix + 'DEST')
    base_url = config.get(prefix + 'URL')
    if destination is None:
        if uset.default_dest:
            destination = uset.default_dest(app)
        if destination is None:
            if defaults['dest'] is not None:
                using_defaults = True
                destination = os.path.join(defaults['dest'], uset.name)
            else:
                raise RuntimeError('no destination for set %s' % uset.name)
    if base_url is None and using_defaults and defaults['url']:
        base_url = addslash(defaults['url']) + uset.name + '/'
    return UploadConfiguration(destination, base_url, allow_extns, deny_extns)