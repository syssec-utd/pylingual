def activate(backend):
    """activate a backend by adding it to the .sregistry configuration file.
    """
    settings = read_client_secrets()
    if backend is not None:
        settings['SREGISTRY_CLIENT'] = backend
        update_secrets(settings)
        print('[activate] %s' % backend)