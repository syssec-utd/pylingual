def set(members: Iterable[T], meta=None) -> Set[T]:
    """Creates a new set."""
    return Set(pset(members), meta=meta)