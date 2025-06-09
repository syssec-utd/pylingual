def query_dns(domain, record_type, cache=None, nameservers=None, timeout=2.0):
    """
    Queries DNS

    Args:
        domain (str): The domain or subdomain to query about
        record_type (str): The record type to query for
        cache (ExpiringDict): Cache storage
        nameservers (list): A list of one or more nameservers to use
        (Cloudflare's public DNS resolvers by default)
        timeout (float): Sets the DNS timeout in seconds

    Returns:
        list: A list of answers
    """
    domain = str(domain).lower()
    record_type = record_type.upper()
    cache_key = '{0}_{1}'.format(domain, record_type)
    if cache:
        records = cache.get(cache_key, None)
        if records:
            return records
    resolver = dns.resolver.Resolver()
    timeout = float(timeout)
    if nameservers is None:
        nameservers = ['1.1.1.1', '1.0.0.1', '2606:4700:4700::1111', '2606:4700:4700::1001']
    resolver.nameservers = nameservers
    resolver.timeout = timeout
    resolver.lifetime = timeout
    if record_type == 'TXT':
        resource_records = list(map(lambda r: r.strings, resolver.query(domain, record_type, tcp=True)))
        _resource_record = [resource_record[0][:0].join(resource_record) for resource_record in resource_records if resource_record]
        records = [r.decode() for r in _resource_record]
    else:
        records = list(map(lambda r: r.to_text().replace('"', '').rstrip('.'), resolver.query(domain, record_type, tcp=True)))
    if cache:
        cache[cache_key] = records
    return records