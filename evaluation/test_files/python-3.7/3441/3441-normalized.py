def tempo(y=None, sr=22050, onset_envelope=None, hop_length=512, start_bpm=120, std_bpm=1.0, ac_size=8.0, max_tempo=320.0, aggregate=np.mean):
    """Estimate the tempo (beats per minute)

    Parameters
    ----------
    y : np.ndarray [shape=(n,)] or None
        audio time series

    sr : number > 0 [scalar]
        sampling rate of the time series

    onset_envelope    : np.ndarray [shape=(n,)]
        pre-computed onset strength envelope

    hop_length : int > 0 [scalar]
        hop length of the time series

    start_bpm : float [scalar]
        initial guess of the BPM

    std_bpm : float > 0 [scalar]
        standard deviation of tempo distribution

    ac_size : float > 0 [scalar]
        length (in seconds) of the auto-correlation window

    max_tempo : float > 0 [scalar, optional]
        If provided, only estimate tempo below this threshold

    aggregate : callable [optional]
        Aggregation function for estimating global tempo.
        If `None`, then tempo is estimated independently for each frame.

    Returns
    -------
    tempo : np.ndarray [scalar]
        estimated tempo (beats per minute)

    See Also
    --------
    librosa.onset.onset_strength
    librosa.feature.tempogram

    Notes
    -----
    This function caches at level 30.

    Examples
    --------
    >>> # Estimate a static tempo
    >>> y, sr = librosa.load(librosa.util.example_audio_file())
    >>> onset_env = librosa.onset.onset_strength(y, sr=sr)
    >>> tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
    >>> tempo
    array([129.199])

    >>> # Or a dynamic tempo
    >>> dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr,
    ...                             aggregate=None)
    >>> dtempo
    array([ 143.555,  143.555,  143.555, ...,  161.499,  161.499,
            172.266])


    Plot the estimated tempo against the onset autocorrelation

    >>> import matplotlib.pyplot as plt
    >>> # Convert to scalar
    >>> tempo = np.asscalar(tempo)
    >>> # Compute 2-second windowed autocorrelation
    >>> hop_length = 512
    >>> ac = librosa.autocorrelate(onset_env, 2 * sr // hop_length)
    >>> freqs = librosa.tempo_frequencies(len(ac), sr=sr,
    ...                                   hop_length=hop_length)
    >>> # Plot on a BPM axis.  We skip the first (0-lag) bin.
    >>> plt.figure(figsize=(8,4))
    >>> plt.semilogx(freqs[1:], librosa.util.normalize(ac)[1:],
    ...              label='Onset autocorrelation', basex=2)
    >>> plt.axvline(tempo, 0, 1, color='r', alpha=0.75, linestyle='--',
    ...            label='Tempo: {:.2f} BPM'.format(tempo))
    >>> plt.xlabel('Tempo (BPM)')
    >>> plt.grid()
    >>> plt.title('Static tempo estimation')
    >>> plt.legend(frameon=True)
    >>> plt.axis('tight')

    Plot dynamic tempo estimates over a tempogram

    >>> plt.figure()
    >>> tg = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr,
    ...                                hop_length=hop_length)
    >>> librosa.display.specshow(tg, x_axis='time', y_axis='tempo')
    >>> plt.plot(librosa.frames_to_time(np.arange(len(dtempo))), dtempo,
    ...          color='w', linewidth=1.5, label='Tempo estimate')
    >>> plt.title('Dynamic tempo estimation')
    >>> plt.legend(frameon=True, framealpha=0.75)
    """
    if start_bpm <= 0:
        raise ParameterError('start_bpm must be strictly positive')
    win_length = np.asscalar(core.time_to_frames(ac_size, sr=sr, hop_length=hop_length))
    tg = tempogram(y=y, sr=sr, onset_envelope=onset_envelope, hop_length=hop_length, win_length=win_length)
    if aggregate is not None:
        tg = aggregate(tg, axis=1, keepdims=True)
    bpms = core.tempo_frequencies(tg.shape[0], hop_length=hop_length, sr=sr)
    prior = np.exp(-0.5 * ((np.log2(bpms) - np.log2(start_bpm)) / std_bpm) ** 2)
    if max_tempo is not None:
        max_idx = np.argmax(bpms < max_tempo)
        prior[:max_idx] = 0
    best_period = np.argmax(tg * prior[:, np.newaxis], axis=0)
    tempi = bpms[best_period]
    tempi[best_period == 0] = start_bpm
    return tempi