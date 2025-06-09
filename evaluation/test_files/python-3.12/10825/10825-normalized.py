def get(name):
    """
    Returns a matcher instance by class or alias name.

    Arguments:
        name (str): matcher class name or alias.

    Returns:
        matcher: found matcher instance, otherwise ``None``.
    """
    for matcher in matchers:
        if matcher.__name__ == name or getattr(matcher, 'name', None) == name:
            return matcher