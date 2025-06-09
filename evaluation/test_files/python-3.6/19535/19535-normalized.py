def check_type(self, type):
    """Check to see if the type is either in TYPES or fits type name

        Returns proper type
        """
    if type in TYPES:
        return type
    tdict = dict(zip(TYPES, TYPES))
    tdict.update({'line': 'lc', 'bar': 'bvs', 'pie': 'p', 'venn': 'v', 'scater': 's', 'radar': 'r', 'meter': 'gom'})
    assert type in tdict, 'Invalid chart type: %s' % type
    return tdict[type]