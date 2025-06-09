def _add_https(self, q):
    """for push, pull, and other api interactions, the user can optionally
           define a custom registry. If the registry name doesn't include http
           or https, add it.
 
           Parameters
           ==========
           q: the parsed image query (names), including the original
        """
    if not q['registry'].startswith('http'):
        if q['original'].startswith('http:'):
            q['registry'] = 'http://%s' % q['registry']
        elif q['original'].startswith('https:'):
            q['registry'] = 'https://%s' % q['registry']
        else:
            prefix = 'https://'
            nohttps = os.environ.get('SREGISTRY_REGISTRY_NOHTTPS')
            if nohttps != None:
                prefix = 'http://'
            q['registry'] = '%s%s' % (prefix, q['registry'])
    return q