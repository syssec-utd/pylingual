def _front_id_from_idx(front, index):
    """
    Returns the front ID found in `front` at the given `index`.

    :param front:               An onset or offset front array of shape [nfrequencies, nsamples]
    :index:                     A tuple of the form (frequency index, sample index)
    :returns:                   The ID of the front or -1 if not found in `front` and the item at `onsets_or_offsets[index]`
                                is not a 1.
    """
    (fidx, sidx) = index
    id = front[fidx, sidx]
    if id == 0:
        return -1
    else:
        return id