def parse_info(wininfo_name, egginfo_name):
    """Extract metadata from filenames.
    
    Extracts the 4 metadataitems needed (name, version, pyversion, arch) from
    the installer filename and the name of the egg-info directory embedded in
    the zipfile (if any).

    The egginfo filename has the format::

        name-ver(-pyver)(-arch).egg-info

    The installer filename has the format::

        name-ver.arch(-pyver).exe

    Some things to note:

    1. The installer filename is not definitive. An installer can be renamed
       and work perfectly well as an installer. So more reliable data should
       be used whenever possible.
    2. The egg-info data should be preferred for the name and version, because
       these come straight from the distutils metadata, and are mandatory.
    3. The pyver from the egg-info data should be ignored, as it is
       constructed from the version of Python used to build the installer,
       which is irrelevant - the installer filename is correct here (even to
       the point that when it's not there, any version is implied).
    4. The architecture must be taken from the installer filename, as it is
       not included in the egg-info data.
    5. Architecture-neutral installers still have an architecture because the
       installer format itself (being executable) is architecture-specific. We
       should therefore ignore the architecture if the content is pure-python.
    """
    egginfo = None
    if egginfo_name:
        egginfo = egg_info_re.search(egginfo_name)
        if not egginfo:
            raise ValueError('Egg info filename %s is not valid' % (egginfo_name,))
    (w_name, sep, rest) = wininfo_name.partition('-')
    if not sep:
        raise ValueError('Installer filename %s is not valid' % (wininfo_name,))
    rest = rest[:-4]
    (rest2, sep, w_pyver) = rest.rpartition('-')
    if sep and w_pyver.startswith('py'):
        rest = rest2
        w_pyver = w_pyver.replace('.', '')
    else:
        w_pyver = 'py2.py3'
    (w_ver, sep, w_arch) = rest.rpartition('.')
    if not sep:
        raise ValueError('Installer filename %s is not valid' % (wininfo_name,))
    if egginfo:
        w_name = egginfo.group('name')
        w_ver = egginfo.group('ver')
    return dict(name=w_name, ver=w_ver, arch=w_arch, pyver=w_pyver)