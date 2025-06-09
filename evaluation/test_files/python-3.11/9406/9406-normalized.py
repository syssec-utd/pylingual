def _match_offset_front_id_to_onset_front_id(onset_front_id, onset_fronts, offset_fronts, onsets, offsets):
    """
    Find all offset fronts which are composed of at least one offset which corresponds to one of the onsets in the
    given onset front.
    The offset front which contains the most of such offsets is the match.
    If there are no such offset fronts, return -1.
    """
    onset_idxs = _get_front_idxs_from_id(onset_fronts, onset_front_id)
    offset_idxs = [_lookup_offset_by_onset_idx(i, onsets, offsets) for i in onset_idxs]
    candidate_offset_front_ids = set([int(offset_fronts[f, i]) for f, i in offset_idxs])
    candidate_offset_front_ids = [id for id in candidate_offset_front_ids if id != 0]
    if candidate_offset_front_ids:
        chosen_offset_front_id = _choose_front_id_from_candidates(candidate_offset_front_ids, offset_fronts, offset_idxs)
    else:
        chosen_offset_front_id = _get_offset_front_id_after_onset_front(onset_front_id, onset_fronts, offset_fronts)
    return chosen_offset_front_id