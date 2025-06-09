def harmonics_2d(harmonic_out, x, freqs, h_range, kind='linear', fill_value=0, axis=0):
    """Populate a harmonic tensor from a time-frequency representation with
    time-varying frequencies.

    Parameters
    ----------
    harmonic_out : np.ndarray
        The output array to store harmonics

    x : np.ndarray
        The input energy

    freqs : np.ndarray, shape=x.shape
        The frequency values corresponding to each element of `x`

    h_range : list-like, non-negative
        Harmonics to compute.  The first harmonic (1) corresponds to `x`
        itself.  Values less than one (e.g., 1/2) correspond to
        sub-harmonics.

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
    harmonics_1d
    """
    idx_in = [slice(None)] * x.ndim
    idx_freq = [slice(None)] * x.ndim
    idx_out = [slice(None)] * harmonic_out.ndim
    ni_axis = (1 + axis) % x.ndim
    for i in range(x.shape[ni_axis]):
        idx_in[ni_axis] = slice(i, i + 1)
        idx_freq[ni_axis] = i
        idx_out[1 + ni_axis] = idx_in[ni_axis]
        harmonics_1d(harmonic_out[tuple(idx_out)], x[tuple(idx_in)], freqs[tuple(idx_freq)], h_range, kind=kind, fill_value=fill_value, axis=axis)