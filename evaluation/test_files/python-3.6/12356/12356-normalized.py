def create_index(idx_url, clean=False):
    """Configure the index to work with"""
    try:
        r = requests.get(idx_url)
    except requests.exceptions.ConnectionError:
        cause = 'Error connecting to Elastic Search (index: %s)' % idx_url
        raise ElasticSearchError(cause=cause)
    if r.status_code != 200:
        r = requests.put(idx_url)
        if r.status_code != 200:
            logger.info("Can't create index %s (%s)", idx_url, r.status_code)
            cause = 'Error creating Elastic Search index %s' % idx_url
            raise ElasticSearchError(cause=cause)
        logger.info('Index %s created', idx_url)
        return True
    elif r.status_code == 200 and clean:
        requests.delete(idx_url)
        requests.put(idx_url)
        logger.info('Index deleted and created (index: %s)', idx_url)
        return True
    return False