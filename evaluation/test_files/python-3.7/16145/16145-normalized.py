def parse_editable(editable_req, default_vcs=None):
    """Parses an editable requirement into:
        - a requirement name
        - an URL
        - extras
        - editable options
    Accepted requirements:
        svn+http://blahblah@rev#egg=Foobar[baz]&subdirectory=version_subdir
        .[some_extra]
    """
    url = editable_req
    extras = None
    m = re.match('^(.+)(\\[[^\\]]+\\])$', url)
    if m:
        url_no_extras = m.group(1)
        extras = m.group(2)
    else:
        url_no_extras = url
    if os.path.isdir(url_no_extras):
        if not os.path.exists(os.path.join(url_no_extras, 'setup.py')):
            raise InstallationError("Directory %r is not installable. File 'setup.py' not found." % url_no_extras)
        url_no_extras = path_to_url(url_no_extras)
    if url_no_extras.lower().startswith('file:'):
        if extras:
            return (None, url_no_extras, pkg_resources.Requirement.parse('__placeholder__' + extras).extras, {})
        else:
            return (None, url_no_extras, None, {})
    for version_control in vcs:
        if url.lower().startswith('%s:' % version_control):
            url = '%s+%s' % (version_control, url)
            break
    if '+' not in url:
        if default_vcs:
            url = default_vcs + '+' + url
        else:
            raise InstallationError('%s should either be a path to a local project or a VCS url beginning with svn+, git+, hg+, or bzr+' % editable_req)
    vc_type = url.split('+', 1)[0].lower()
    if not vcs.get_backend(vc_type):
        error_message = 'For --editable=%s only ' % editable_req + ', '.join([backend.name + '+URL' for backend in vcs.backends]) + ' is currently supported'
        raise InstallationError(error_message)
    try:
        options = _build_editable_options(editable_req)
    except Exception as exc:
        raise InstallationError('--editable=%s error in editable options:%s' % (editable_req, exc))
    if not options or 'egg' not in options:
        req = _build_req_from_url(editable_req)
        if not req:
            raise InstallationError('--editable=%s is not the right format; it must have #egg=Package' % editable_req)
    else:
        req = options['egg']
    package = _strip_postfix(req)
    return (package, url, None, options)