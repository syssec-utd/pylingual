def l(*members, meta=None) -> List:
    """Creates a new list from members."""
    return List(plist(iterable=members), meta=meta)