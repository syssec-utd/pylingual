def fetch_config(zone, conn):
    """Fetch all pieces of a Route 53 config from Amazon.

  Args: zone: string, hosted zone id.
        conn: boto.route53.Route53Connection
  Returns: list of ElementTrees, one for each piece of config."""
    more_to_fetch = True
    cfg_chunks = []
    next_name = None
    next_type = None
    next_identifier = None
    while more_to_fetch == True:
        more_to_fetch = False
        getstr = '/%s/hostedzone/%s/rrset' % (R53_API_VERSION, zone)
        if next_name is not None:
            getstr += '?name=%s&type=%s' % (next_name, next_type)
            if next_identifier is not None:
                getstr += '&identifier=%s' % next_identifier
        log.debug('requesting %s' % getstr)
        resp = conn.make_request('GET', getstr)
        etree = lxml.etree.parse(resp)
        cfg_chunks.append(etree)
        root = etree.getroot()
        truncated = root.find('{%s}IsTruncated' % R53_XMLNS)
        if truncated is not None and truncated.text == 'true':
            more_to_fetch = True
            next_name = root.find('{%s}NextRecordName' % R53_XMLNS).text
            next_type = root.find('{%s}NextRecordType' % R53_XMLNS).text
            try:
                next_identifier = root.find('{%s}NextRecordIdentifier' % R53_XMLNS).text
            except AttributeError:
                next_identifier = None
    return cfg_chunks