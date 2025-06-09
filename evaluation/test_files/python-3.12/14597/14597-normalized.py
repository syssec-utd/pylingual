def split_with_locations(text, locations):
    """
    Use an integer list to split the string
    contained in `text`.

    Arguments:
    ----------
        text : str, same length as locations.
        locations : list<int>, contains values
            'SHOULD_SPLIT', 'UNDECIDED', and
            'SHOULD_NOT_SPLIT'. Will create
            strings between each 'SHOULD_SPLIT'
            locations.
    Returns:
    --------
        Generator<str> : the substrings of text
            corresponding to the slices given
            in locations.
    """
    start = 0
    for pos, decision in enumerate(locations):
        if decision == SHOULD_SPLIT:
            if start != pos:
                yield text[start:pos]
            start = pos
    if start != len(text):
        yield text[start:]