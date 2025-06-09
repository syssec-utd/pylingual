def window_bandwidth(window, n=1000):
    """Get the equivalent noise bandwidth of a window function.


    Parameters
    ----------
    window : callable or string
        A window function, or the name of a window function.
        Examples:
        - scipy.signal.hann
        - 'boxcar'

    n : int > 0
        The number of coefficients to use in estimating the
        window bandwidth

    Returns
    -------
    bandwidth : float
        The equivalent noise bandwidth (in FFT bins) of the
        given window function

    Notes
    -----
    This function caches at level 10.

    See Also
    --------
    get_window
    """
    if hasattr(window, '__name__'):
        key = window.__name__
    else:
        key = window
    if key not in WINDOW_BANDWIDTHS:
        win = get_window(window, n)
        WINDOW_BANDWIDTHS[key] = n * np.sum(win ** 2) / np.sum(np.abs(win)) ** 2
    return WINDOW_BANDWIDTHS[key]