def mme_nodes(mme_base_url, token):
    """Return the available MatchMaker nodes

    Args:
        mme_base_url(str): base URL of MME service
        token(str): MME server authorization token

    Returns:
        nodes(list): a list of node disctionaries
    """
    nodes = []
    if not mme_base_url or not token:
        return nodes
    url = ''.join([mme_base_url, '/nodes'])
    nodes = matchmaker_request(url=url, token=token, method='GET')
    LOG.info('Matchmaker has the following connected nodes:{}'.format(nodes))
    return nodes