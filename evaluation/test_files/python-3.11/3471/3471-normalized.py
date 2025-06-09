def sync(data, idx, aggregate=None, pad=True, axis=-1):
    """Synchronous aggregation of a multi-dimensional array between boundaries

    .. note::
        In order to ensure total coverage, boundary points may be added
        to `idx`.

        If synchronizing a feature matrix against beat tracker output, ensure
        that frame index numbers are properly aligned and use the same hop length.

    Parameters
    ----------
    data      : np.ndarray
        multi-dimensional array of features

    idx : iterable of ints or slices
        Either an ordered array of boundary indices, or
        an iterable collection of slice objects.


    aggregate : function
        aggregation function (default: `np.mean`)

    pad : boolean
        If `True`, `idx` is padded to span the full range `[0, data.shape[axis]]`

    axis : int
        The axis along which to aggregate data

    Returns
    -------
    data_sync : ndarray
        `data_sync` will have the same dimension as `data`, except that the `axis`
        coordinate will be reduced according to `idx`.

        For example, a 2-dimensional `data` with `axis=-1` should satisfy

        `data_sync[:, i] = aggregate(data[:, idx[i-1]:idx[i]], axis=-1)`

    Raises
    ------
    ParameterError
        If the index set is not of consistent type (all slices or all integers)

    Notes
    -----
    This function caches at level 40.

    Examples
    --------
    Beat-synchronous CQT spectra

    >>> y, sr = librosa.load(librosa.util.example_audio_file())
    >>> tempo, beats = librosa.beat.beat_track(y=y, sr=sr, trim=False)
    >>> C = np.abs(librosa.cqt(y=y, sr=sr))
    >>> beats = librosa.util.fix_frames(beats, x_max=C.shape[1])

    By default, use mean aggregation

    >>> C_avg = librosa.util.sync(C, beats)

    Use median-aggregation instead of mean

    >>> C_med = librosa.util.sync(C, beats,
    ...                             aggregate=np.median)

    Or sub-beat synchronization

    >>> sub_beats = librosa.segment.subsegment(C, beats)
    >>> sub_beats = librosa.util.fix_frames(sub_beats, x_max=C.shape[1])
    >>> C_med_sub = librosa.util.sync(C, sub_beats, aggregate=np.median)


    Plot the results

    >>> import matplotlib.pyplot as plt
    >>> beat_t = librosa.frames_to_time(beats, sr=sr)
    >>> subbeat_t = librosa.frames_to_time(sub_beats, sr=sr)
    >>> plt.figure()
    >>> plt.subplot(3, 1, 1)
    >>> librosa.display.specshow(librosa.amplitude_to_db(C,
    ...                                                  ref=np.max),
    ...                          x_axis='time')
    >>> plt.title('CQT power, shape={}'.format(C.shape))
    >>> plt.subplot(3, 1, 2)
    >>> librosa.display.specshow(librosa.amplitude_to_db(C_med,
    ...                                                  ref=np.max),
    ...                          x_coords=beat_t, x_axis='time')
    >>> plt.title('Beat synchronous CQT power, '
    ...           'shape={}'.format(C_med.shape))
    >>> plt.subplot(3, 1, 3)
    >>> librosa.display.specshow(librosa.amplitude_to_db(C_med_sub,
    ...                                                  ref=np.max),
    ...                          x_coords=subbeat_t, x_axis='time')
    >>> plt.title('Sub-beat synchronous CQT power, '
    ...           'shape={}'.format(C_med_sub.shape))
    >>> plt.tight_layout()

    """
    if aggregate is None:
        aggregate = np.mean
    shape = list(data.shape)
    if np.all([isinstance(_, slice) for _ in idx]):
        slices = idx
    elif np.all([np.issubdtype(type(_), np.integer) for _ in idx]):
        slices = index_to_slice(np.asarray(idx), 0, shape[axis], pad=pad)
    else:
        raise ParameterError('Invalid index set: {}'.format(idx))
    agg_shape = list(shape)
    agg_shape[axis] = len(slices)
    data_agg = np.empty(agg_shape, order='F' if np.isfortran(data) else 'C', dtype=data.dtype)
    idx_in = [slice(None)] * data.ndim
    idx_agg = [slice(None)] * data_agg.ndim
    for i, segment in enumerate(slices):
        idx_in[axis] = segment
        idx_agg[axis] = i
        data_agg[tuple(idx_agg)] = aggregate(data[tuple(idx_in)], axis=axis)
    return data_agg