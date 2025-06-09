def items_to_dict(items):
    """
    Converts list of tuples to dictionary with duplicate keys converted to
    lists.

    :param list items:
        List of tuples.

    :returns:
        :class:`dict`

    """
    res = collections.defaultdict(list)
    for k, v in items:
        res[k].append(v)
    return normalize_dict(dict(res))