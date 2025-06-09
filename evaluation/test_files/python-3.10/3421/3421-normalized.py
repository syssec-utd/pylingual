def harmonics_1d(harmonic_out, x, freqs, h_range, kind='linear', fill_value=0, axis=0):
    """Populate a harmonic tensor from a time-frequency representation.

    Parameters
    ----------
    harmonic_out : np.ndarray, shape=(len(h_range), X.shape)
        The output array to store harmonics

    X : np.ndarray
        The input energy

    freqs : np.ndarray, shape=(x.shape[axis])
        The frequency values corresponding to x's elements along the
        chosen axis.

    h_range : list-like, non-negative
        Harmonics to compute.  The first harmonic (1) corresponds to `x`
        itself.
        Values less than one (e.g., 1/2) correspond to sub-harmonics.

    kind : str
        Interpolation type.  See `scipy.interpolate.interp1d`.

    fill_value : float
        The value to fill when extrapolating beyond the observed
        frequency range.

    axis : int
        The axis along which to compute harmonics

    See Also
    --------
    harmonics
    scipy.interpolate.interp1d


    Examples
    --------
    Estimate the harmonics of a time-averaged tempogram

    >>> y, sr = librosa.load(librosa.util.example_audio_file(),
    ...                      duration=15, offset=30)
    >>> # Compute the time-varying tempogram and average over time
    >>> tempi = np.mean(librosa.feature.tempogram(y=y, sr=sr), axis=1)
    >>> # We'll measure the first five harmonics
    >>> h_range = [1, 2, 3, 4, 5]
    >>> f_tempo = librosa.tempo_frequencies(len(tempi), sr=sr)
    >>> # Build the harmonic tensor
    >>> t_harmonics = librosa.interp_harmonics(tempi, f_tempo, h_range)
    >>> print(t_harmonics.shape)
    (5, 384)

    >>> # And plot the results
    >>> import matplotlib.pyplot as plt
    >>> plt.figure()
    >>> librosa.display.specshow(t_harmonics, x_axis='tempo', sr=sr)
    >>> plt.yticks(0.5 + np.arange(len(h_range)),
    ...            ['{:.3g}'.format(_) for _ in h_range])
    >>> plt.ylabel('Harmonic')
    >>> plt.xlabel('Tempo (BPM)')
    >>> plt.tight_layout()

    We can also compute frequency harmonics for spectrograms.
    To calculate subharmonic energy, use values < 1.

    >>> h_range = [1./3, 1./2, 1, 2, 3, 4]
    >>> S = np.abs(librosa.stft(y))
    >>> fft_freqs = librosa.fft_frequencies(sr=sr)
    >>> S_harm = librosa.interp_harmonics(S, fft_freqs, h_range, axis=0)
    >>> print(S_harm.shape)
    (6, 1025, 646)

    >>> plt.figure()
    >>> for i, _sh in enumerate(S_harm, 1):
    ...     plt.subplot(3,2,i)
    ...     librosa.display.specshow(librosa.amplitude_to_db(_sh,
    ...                                                      ref=S.max()),
    ...                              sr=sr, y_axis='log')
    ...     plt.title('h={:.3g}'.format(h_range[i-1]))
    ...     plt.yticks([])
    >>> plt.tight_layout()
    """
    f_interp = scipy.interpolate.interp1d(freqs, x, kind=kind, axis=axis, copy=False, bounds_error=False, fill_value=fill_value)
    idx_out = [slice(None)] * harmonic_out.ndim
    interp_axis = 1 + axis % x.ndim
    for (h_index, harmonic) in enumerate(h_range):
        idx_out[0] = h_index
        for (f_index, frequency) in enumerate(freqs):
            idx_out[interp_axis] = f_index
            harmonic_out[tuple(idx_out)] = f_interp(harmonic * frequency)