def matches_count(count, options):
    """
    Returns whether the given count matches the given query options.

    If no quantity options are specified, any count is considered acceptable.

    Args:
        count (int): The count to be validated.
        options (Dict[str, int | Iterable[int]]): A dictionary of query options.

    Returns:
        bool: Whether the count matches the options.
    """
    if options.get('count') is not None:
        return count == int(options['count'])
    if options.get('maximum') is not None and int(options['maximum']) < count:
        return False
    if options.get('minimum') is not None and int(options['minimum']) > count:
        return False
    if options.get('between') is not None and count not in options['between']:
        return False
    return True