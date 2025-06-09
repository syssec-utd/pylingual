def _make_stream_items(f):
    """Given a spinn3r feed, produce a sequence of valid StreamItems.

    Because of goopy Python interactions, you probably need to call
    this and re-yield its results, as

    >>> with open(filename, 'rb') as f:
    ...   for si in _make_stream_items(f):
    ...     yield si

    """
    reader = ProtoStreamReader(f)
    return itertools.ifilter(lambda x: x is not None, itertools.imap(_make_stream_item, reader))