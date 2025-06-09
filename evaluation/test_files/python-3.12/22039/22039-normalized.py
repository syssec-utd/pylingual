def get_installed_version(name):
    """
        returns installed package version and None if package is not installed
    """
    pattern = re.compile('Installed:\\s+(?P<version>.*)')
    cmd = 'apt-cache policy %s' % name
    args = shlex.split(cmd)
    try:
        output = subprocess.check_output(args)
        if not output:
            return None
    except CalledProcessError:
        return None
    match = pattern.search(output)
    if match:
        version = match.groupdict()['version']
        if version == '(none)':
            return None
        else:
            return version