def samples_like(X, hop_length=512, n_fft=None, axis=-1):
    """Return an array of sample indices to match the time axis from a feature matrix.

    Parameters
    ----------
    X : np.ndarray or scalar
        - If ndarray, X is a feature matrix, e.g. STFT, chromagram, or mel spectrogram.
        - If scalar, X represents the number of frames.

    hop_length : int > 0 [scalar]
        number of samples between successive frames

    n_fft : None or int > 0 [scalar]
        Optional: length of the FFT window.
        If given, time conversion will include an offset of `n_fft / 2`
        to counteract windowing effects when using a non-centered STFT.

    axis : int [scalar]
        The axis representing the time axis of X.
        By default, the last axis (-1) is taken.

    Returns
    -------
    samples : np.ndarray [shape=(n,)]
        ndarray of sample indices corresponding to each frame of X.

    See Also
    --------
    times_like : Return an array of time values to match the time axis from a feature matrix.

    Examples
    --------
    Provide a feature matrix input:

    >>> y, sr = librosa.load(librosa.util.example_audio_file())
    >>> X = librosa.stft(y)
    >>> samples = librosa.samples_like(X)
    >>> samples
    array([      0,     512,    1024, ..., 1353728, 1354240, 1354752])

    Provide a scalar input:

    >>> n_frames = 2647
    >>> samples = librosa.samples_like(n_frames)
    >>> samples
    array([      0,     512,    1024, ..., 1353728, 1354240, 1354752])
    """
    if np.isscalar(X):
        frames = np.arange(X)
    else:
        frames = np.arange(X.shape[axis])
    return frames_to_samples(frames, hop_length=hop_length, n_fft=n_fft)