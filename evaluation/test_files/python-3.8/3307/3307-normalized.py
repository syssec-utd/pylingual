def cqt_frequencies(n_bins, fmin, bins_per_octave=12, tuning=0.0):
    """Compute the center frequencies of Constant-Q bins.

    Examples
    --------
    >>> # Get the CQT frequencies for 24 notes, starting at C2
    >>> librosa.cqt_frequencies(24, fmin=librosa.note_to_hz('C2'))
    array([  65.406,   69.296,   73.416,   77.782,   82.407,   87.307,
             92.499,   97.999,  103.826,  110.   ,  116.541,  123.471,
            130.813,  138.591,  146.832,  155.563,  164.814,  174.614,
            184.997,  195.998,  207.652,  220.   ,  233.082,  246.942])

    Parameters
    ----------
    n_bins  : int > 0 [scalar]
        Number of constant-Q bins

    fmin    : float > 0 [scalar]
        Minimum frequency

    bins_per_octave : int > 0 [scalar]
        Number of bins per octave

    tuning : float in `[-0.5, +0.5)`
        Deviation from A440 tuning in fractional bins (cents)

    Returns
    -------
    frequencies : np.ndarray [shape=(n_bins,)]
        Center frequency for each CQT bin
    """
    correction = 2.0 ** (float(tuning) / bins_per_octave)
    frequencies = 2.0 ** (np.arange(0, n_bins, dtype=float) / bins_per_octave)
    return correction * fmin * frequencies