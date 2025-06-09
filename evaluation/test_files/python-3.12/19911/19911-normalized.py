def pretty_string(fc):
    """construct a nice looking string for an FC
    """
    s = []
    for fname, feature in sorted(fc.items()):
        if isinstance(feature, StringCounter):
            feature = [u'%s: %d' % (k, v) for k, v in feature.most_common()]
            feature = u'\n\t' + u'\n\t'.join(feature)
        s.append(fname + u': ' + feature)
    return u'\n'.join(s)