def stft(y, n_fft=2048, hop_length=None, win_length=None, window='hann', center=True, dtype=np.complex64, pad_mode='reflect'):
    """Short-time Fourier transform (STFT)

    Returns a complex-valued matrix D such that
        `np.abs(D[f, t])` is the magnitude of frequency bin `f`
        at frame `t`

        `np.angle(D[f, t])` is the phase of frequency bin `f`
        at frame `t`

    Parameters
    ----------
    y : np.ndarray [shape=(n,)], real-valued
        the input signal (audio time series)

    n_fft : int > 0 [scalar]
        FFT window size

    hop_length : int > 0 [scalar]
        number audio of frames between STFT columns.
        If unspecified, defaults `win_length / 4`.

    win_length : int <= n_fft [scalar]
        Each frame of audio is windowed by `window()`.
        The window will be of length `win_length` and then padded
        with zeros to match `n_fft`.

        If unspecified, defaults to ``win_length = n_fft``.

    window : string, tuple, number, function, or np.ndarray [shape=(n_fft,)]
        - a window specification (string, tuple, or number);
          see `scipy.signal.get_window`
        - a window function, such as `scipy.signal.hanning`
        - a vector or array of length `n_fft`

        .. see also:: `filters.get_window`

    center : boolean
        - If `True`, the signal `y` is padded so that frame
          `D[:, t]` is centered at `y[t * hop_length]`.
        - If `False`, then `D[:, t]` begins at `y[t * hop_length]`

    dtype : numeric type
        Complex numeric type for `D`.  Default is 64-bit complex.

    pad_mode : string
        If `center=True`, the padding mode to use at the edges of the signal.
        By default, STFT uses reflection padding.


    Returns
    -------
    D : np.ndarray [shape=(1 + n_fft/2, t), dtype=dtype]
        STFT matrix


    See Also
    --------
    istft : Inverse STFT

    ifgram : Instantaneous frequency spectrogram

    np.pad : array padding

    Notes
    -----
    This function caches at level 20.


    Examples
    --------

    >>> y, sr = librosa.load(librosa.util.example_audio_file())
    >>> D = np.abs(librosa.stft(y))
    >>> D
    array([[2.58028018e-03, 4.32422794e-02, 6.61255598e-01, ...,
            6.82710262e-04, 2.51654536e-04, 7.23036574e-05],
           [2.49403086e-03, 5.15930466e-02, 6.00107312e-01, ...,
            3.48026224e-04, 2.35853557e-04, 7.54836728e-05],
           [7.82410789e-04, 1.05394892e-01, 4.37517226e-01, ...,
            6.29352580e-04, 3.38571583e-04, 8.38094638e-05],
           ...,
           [9.48568513e-08, 4.74725084e-07, 1.50052492e-05, ...,
            1.85637656e-08, 2.89708542e-08, 5.74304337e-09],
           [1.25165826e-07, 8.58259284e-07, 1.11157215e-05, ...,
            3.49099771e-08, 3.11740926e-08, 5.29926236e-09],
           [1.70630571e-07, 8.92518756e-07, 1.23656537e-05, ...,
            5.33256745e-08, 3.33264900e-08, 5.13272980e-09]], dtype=float32)


    Use left-aligned frames, instead of centered frames

    >>> D_left = np.abs(librosa.stft(y, center=False))


    Use a shorter hop length

    >>> D_short = np.abs(librosa.stft(y, hop_length=64))


    Display a spectrogram

    >>> import matplotlib.pyplot as plt
    >>> librosa.display.specshow(librosa.amplitude_to_db(D,
    ...                                                  ref=np.max),
    ...                          y_axis='log', x_axis='time')
    >>> plt.title('Power spectrogram')
    >>> plt.colorbar(format='%+2.0f dB')
    >>> plt.tight_layout()

    """
    if win_length is None:
        win_length = n_fft
    if hop_length is None:
        hop_length = int(win_length // 4)
    fft_window = get_window(window, win_length, fftbins=True)
    fft_window = util.pad_center(fft_window, n_fft)
    fft_window = fft_window.reshape((-1, 1))
    util.valid_audio(y)
    if center:
        y = np.pad(y, int(n_fft // 2), mode=pad_mode)
    y_frames = util.frame(y, frame_length=n_fft, hop_length=hop_length)
    stft_matrix = np.empty((int(1 + n_fft // 2), y_frames.shape[1]), dtype=dtype, order='F')
    fft = get_fftlib()
    n_columns = int(util.MAX_MEM_BLOCK / (stft_matrix.shape[0] * stft_matrix.itemsize))
    for bl_s in range(0, stft_matrix.shape[1], n_columns):
        bl_t = min(bl_s + n_columns, stft_matrix.shape[1])
        stft_matrix[:, bl_s:bl_t] = fft.rfft(fft_window * y_frames[:, bl_s:bl_t], axis=0)
    return stft_matrix