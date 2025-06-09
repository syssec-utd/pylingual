def parse_yaml_linenumbers(data, filename):
    """Parses yaml as ansible.utils.parse_yaml but with linenumbers.

    The line numbers are stored in each node's LINE_NUMBER_KEY key.
    """

    def compose_node(parent, index):
        line = loader.line
        node = Composer.compose_node(loader, parent, index)
        node.__line__ = line + 1
        return node

    def construct_mapping(node, deep=False):
        if ANSIBLE_VERSION < 2:
            mapping = Constructor.construct_mapping(loader, node, deep=deep)
        else:
            mapping = AnsibleConstructor.construct_mapping(loader, node, deep=deep)
        if hasattr(node, '__line__'):
            mapping[LINE_NUMBER_KEY] = node.__line__
        else:
            mapping[LINE_NUMBER_KEY] = mapping._line_number
        mapping[FILENAME_KEY] = filename
        return mapping
    try:
        if ANSIBLE_VERSION < 2:
            loader = yaml.Loader(data)
        else:
            import inspect
            kwargs = {}
            if 'vault_password' in inspect.getargspec(AnsibleLoader.__init__).args:
                kwargs['vault_password'] = DEFAULT_VAULT_PASSWORD
            loader = AnsibleLoader(data, **kwargs)
        loader.compose_node = compose_node
        loader.construct_mapping = construct_mapping
        data = loader.get_single_data()
    except (yaml.parser.ParserError, yaml.scanner.ScannerError) as e:
        raise SystemExit('Failed to parse YAML in %s: %s' % (filename, str(e)))
    return data