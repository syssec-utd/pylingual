def _get_offset_front_id_after_onset_front(onset_front_id, onset_fronts, offset_fronts):
    """
    Get the ID corresponding to the offset which occurs first after the given onset_front_id.
    By `first` I mean the front which contains the offset which is closest to the latest point
    in the onset front. By `after`, I mean that the offset must contain only offsets which
    occur after the latest onset in the onset front.

    If there is no appropriate offset front, the id returned is -1.
    """
    onset_idxs = _get_front_idxs_from_id(onset_fronts, onset_front_id)
    onset_sample_idxs = [s for _f, s in onset_idxs]
    latest_onset_in_front = max(onset_sample_idxs)
    offset_front_id_after_this_onset_front = _get_offset_front_id_after_onset_sample_idx(latest_onset_in_front, offset_fronts)
    return int(offset_front_id_after_this_onset_front)