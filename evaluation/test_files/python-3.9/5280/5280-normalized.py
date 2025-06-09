def split_at(it, split_value):
    """Splits an iterator C{it} at values of C{split_value}. 

    Each instance of C{split_value} is swallowed. The iterator produces
    subiterators which need to be consumed fully before the next subiterator
    can be used.
    """

    def _chunk_iterator(first):
        v = first
        while v != split_value:
            yield v
            v = next(it)
    while True:
        yield _chunk_iterator(next(it))