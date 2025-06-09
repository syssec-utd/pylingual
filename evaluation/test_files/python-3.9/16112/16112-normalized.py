def pkginfo_to_dict(path, distribution=None):
    """
    Convert PKG-INFO to a prototype Metadata 2.0 (PEP 426) dict.

    The description is included under the key ['description'] rather than
    being written to a separate file.

    path: path to PKG-INFO file
    distribution: optional distutils Distribution()
    """
    metadata = defaultdict(lambda : defaultdict(lambda : defaultdict(dict)))
    metadata['generator'] = 'bdist_wheel (' + wheel.__version__ + ')'
    try:
        unicode
        pkg_info = read_pkg_info(path)
    except NameError:
        pkg_info = email.parser.Parser().parsestr(open(path, 'rb').read().decode('utf-8'))
    description = None
    if pkg_info['Summary']:
        metadata['summary'] = pkginfo_unicode(pkg_info, 'Summary')
        del pkg_info['Summary']
    if pkg_info['Description']:
        description = dedent_description(pkg_info)
        del pkg_info['Description']
    else:
        payload = pkg_info.get_payload()
        if isinstance(payload, bytes):
            payload = payload.decode('utf-8')
        if payload:
            description = payload
    if description:
        pkg_info['description'] = description
    for key in unique((k.lower() for k in pkg_info.keys())):
        low_key = key.replace('-', '_')
        if low_key in SKIP_FIELDS:
            continue
        if low_key in UNKNOWN_FIELDS and pkg_info.get(key) == 'UNKNOWN':
            continue
        if low_key in PLURAL_FIELDS:
            metadata[PLURAL_FIELDS[low_key]] = pkg_info.get_all(key)
        elif low_key == 'requires_dist':
            handle_requires(metadata, pkg_info, key)
        elif low_key == 'provides_extra':
            if not 'extras' in metadata:
                metadata['extras'] = []
            metadata['extras'].extend(pkg_info.get_all(key))
        elif low_key == 'home_page':
            metadata['extensions']['python.details']['project_urls'] = {'Home': pkg_info[key]}
        elif low_key == 'keywords':
            metadata['keywords'] = KEYWORDS_RE.split(pkg_info[key])
        else:
            metadata[low_key] = pkg_info[key]
    metadata['metadata_version'] = METADATA_VERSION
    if 'extras' in metadata:
        metadata['extras'] = sorted(set(metadata['extras']))
    if distribution:
        for (requires, attr) in (('test_requires', 'tests_require'),):
            try:
                requirements = getattr(distribution, attr)
                if isinstance(requirements, list):
                    new_requirements = list(convert_requirements(requirements))
                    metadata[requires] = [{'requires': new_requirements}]
            except AttributeError:
                pass
    contacts = []
    for (contact_type, role) in CONTACT_FIELDS:
        contact = {}
        for key in contact_type:
            if contact_type[key] in metadata:
                contact[key] = metadata.pop(contact_type[key])
        if contact:
            contact['role'] = role
            contacts.append(contact)
    if contacts:
        metadata['extensions']['python.details']['contacts'] = contacts
    try:
        with open(os.path.join(os.path.dirname(path), 'entry_points.txt'), 'r') as ep_file:
            ep_map = pkg_resources.EntryPoint.parse_map(ep_file.read())
        exports = {}
        for (group, items) in ep_map.items():
            exports[group] = {}
            for item in items.values():
                (name, export) = str(item).split(' = ', 1)
                exports[group][name] = export
        if exports:
            metadata['extensions']['python.exports'] = exports
    except IOError:
        pass
    if 'python.exports' in metadata['extensions']:
        for (ep_script, wrap_script) in (('console_scripts', 'wrap_console'), ('gui_scripts', 'wrap_gui')):
            if ep_script in metadata['extensions']['python.exports']:
                metadata['extensions']['python.commands'][wrap_script] = metadata['extensions']['python.exports'][ep_script]
    return metadata