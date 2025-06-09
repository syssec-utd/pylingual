def parse_host(host):
    """Parses host name and port number from a string.
    """
    if re.match('^(\\d+)$', host) is not None:
        return ('0.0.0.0', int(host))
    if re.match('^(\\w+)://', host) is None:
        host = '//' + host
    o = parse.urlparse(host)
    hostname = o.hostname or '0.0.0.0'
    port = o.port or 0
    return (hostname, port)