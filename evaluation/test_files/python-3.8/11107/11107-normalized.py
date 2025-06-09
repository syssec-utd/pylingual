def unique_items(seq):
    """Return the unique items from iterable *seq* (in order)."""
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]