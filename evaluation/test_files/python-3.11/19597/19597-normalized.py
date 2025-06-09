def _connected(client):
    """
    Connected to AMP server, start listening locally, and give the AMP
    client a reference to the local listening factory.
    """
    log.msg('Connected to AMP server, starting to listen locally...')
    localFactory = multiplexing.ProxyingFactory(client, 'hello')
    return listeningEndpoint.listen(localFactory)