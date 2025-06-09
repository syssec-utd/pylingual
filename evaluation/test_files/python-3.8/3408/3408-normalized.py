def chroma_cqt(y=None, sr=22050, C=None, hop_length=512, fmin=None, norm=np.inf, threshold=0.0, tuning=None, n_chroma=12, n_octaves=7, window=None, bins_per_octave=None, cqt_mode='full'):
    """Constant-Q chromagram

    Parameters
    ----------
    y : np.ndarray [shape=(n,)]
        audio time series

    sr : number > 0
        sampling rate of `y`

    C : np.ndarray [shape=(d, t)] [Optional]
        a pre-computed constant-Q spectrogram

    hop_length : int > 0
        number of samples between successive chroma frames

    fmin : float > 0
        minimum frequency to analyze in the CQT.
        Default: 'C1' ~= 32.7 Hz

    norm : int > 0, +-np.inf, or None
        Column-wise normalization of the chromagram.

    threshold : float
        Pre-normalization energy threshold.  Values below the
        threshold are discarded, resulting in a sparse chromagram.

    tuning : float
        Deviation (in cents) from A440 tuning

    n_chroma : int > 0
        Number of chroma bins to produce

    n_octaves : int > 0
        Number of octaves to analyze above `fmin`

    window : None or np.ndarray
        Optional window parameter to `filters.cq_to_chroma`

    bins_per_octave : int > 0
        Number of bins per octave in the CQT.
        Default: matches `n_chroma`

    cqt_mode : ['full', 'hybrid']
        Constant-Q transform mode

    Returns
    -------
    chromagram : np.ndarray [shape=(n_chroma, t)]
        The output chromagram

    See Also
    --------
    librosa.util.normalize
    librosa.core.cqt
    librosa.core.hybrid_cqt
    chroma_stft

    Examples
    --------
    Compare a long-window STFT chromagram to the CQT chromagram


    >>> y, sr = librosa.load(librosa.util.example_audio_file(),
    ...                      offset=10, duration=15)
    >>> chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr,
    ...                                           n_chroma=12, n_fft=4096)
    >>> chroma_cq = librosa.feature.chroma_cqt(y=y, sr=sr)

    >>> import matplotlib.pyplot as plt
    >>> plt.figure()
    >>> plt.subplot(2,1,1)
    >>> librosa.display.specshow(chroma_stft, y_axis='chroma')
    >>> plt.title('chroma_stft')
    >>> plt.colorbar()
    >>> plt.subplot(2,1,2)
    >>> librosa.display.specshow(chroma_cq, y_axis='chroma', x_axis='time')
    >>> plt.title('chroma_cqt')
    >>> plt.colorbar()
    >>> plt.tight_layout()

    """
    cqt_func = {'full': cqt, 'hybrid': hybrid_cqt}
    if bins_per_octave is None:
        bins_per_octave = n_chroma
    if C is None:
        C = np.abs(cqt_func[cqt_mode](y, sr=sr, hop_length=hop_length, fmin=fmin, n_bins=n_octaves * bins_per_octave, bins_per_octave=bins_per_octave, tuning=tuning))
    cq_to_chr = filters.cq_to_chroma(C.shape[0], bins_per_octave=bins_per_octave, n_chroma=n_chroma, fmin=fmin, window=window)
    chroma = cq_to_chr.dot(C)
    if threshold is not None:
        chroma[chroma < threshold] = 0.0
    if norm is not None:
        chroma = util.normalize(chroma, norm=norm, axis=0)
    return chroma