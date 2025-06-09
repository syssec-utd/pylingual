def match_events(events_from, events_to, left=True, right=True):
    """Match one set of events to another.

    This is useful for tasks such as matching beats to the nearest
    detected onsets, or frame-aligned events to the nearest zero-crossing.

    .. note:: A target event may be matched to multiple source events.

    Examples
    --------
    >>> # Sources are multiples of 7
    >>> s_from = np.arange(0, 100, 7)
    >>> s_from
    array([ 0,  7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91,
           98])
    >>> # Targets are multiples of 10
    >>> s_to = np.arange(0, 100, 10)
    >>> s_to
    array([ 0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
    >>> # Find the matching
    >>> idx = librosa.util.match_events(s_from, s_to)
    >>> idx
    array([0, 1, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 8, 9, 9])
    >>> # Print each source value to its matching target
    >>> zip(s_from, s_to[idx])
    [(0, 0), (7, 10), (14, 10), (21, 20), (28, 30), (35, 30),
     (42, 40), (49, 50), (56, 60), (63, 60), (70, 70), (77, 80),
     (84, 80), (91, 90), (98, 90)]

    Parameters
    ----------
    events_from : ndarray [shape=(n,)]
      Array of events (eg, times, sample or frame indices) to match from.

    events_to : ndarray [shape=(m,)]
      Array of events (eg, times, sample or frame indices) to
      match against.

    left : bool
    right : bool
        If `False`, then matched events cannot be to the left (or right)
        of source events.

    Returns
    -------
    event_mapping : np.ndarray [shape=(n,)]
        For each event in `events_from`, the corresponding event
        index in `events_to`.

        `event_mapping[i] == arg min |events_from[i] - events_to[:]|`

    See Also
    --------
    match_intervals

    Raises
    ------
    ParameterError
        If either array of input events is not the correct shape
    """
    if len(events_from) == 0 or len(events_to) == 0:
        raise ParameterError('Attempting to match empty event list')
    if not (left or right) and (not np.all(np.in1d(events_from, events_to))):
        raise ParameterError('Cannot match events with left=right=False and events_from is not contained in events_to')
    if not left and max(events_to) < max(events_from):
        raise ParameterError('Cannot match events with left=False and max(events_to) < max(events_from)')
    if not right and min(events_to) > min(events_from):
        raise ParameterError('Cannot match events with right=False and min(events_to) > min(events_from)')
    output = np.empty_like(events_from, dtype=np.int)
    return __match_events_helper(output, events_from, events_to, left, right)