def cache_url(self, **kwargs):
    """A simplified URL to be used for caching the given query."""
    query = {'Operation': self.Operation, 'Service': 'AWSECommerceService', 'Version': self.Version}
    query.update(kwargs)
    service_domain = SERVICE_DOMAINS[self.Region][0]
    return 'http://' + service_domain + '/onca/xml?' + _quote_query(query)