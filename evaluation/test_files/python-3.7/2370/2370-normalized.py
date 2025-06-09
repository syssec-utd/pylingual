def endpoint_groups():
    """Return endpoints, grouped by the class which handles them."""
    groups = defaultdict(list)
    for e in endpoints():
        groups[e['class_name']].append(e)
    return groups