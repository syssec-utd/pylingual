def diagonal_filter(window, n, slope=1.0, angle=None, zero_mean=False):
    """Build a two-dimensional diagonal filter.

    This is primarily used for smoothing recurrence or self-similarity matrices.

    Parameters
    ----------
    window : string, tuple, number, callable, or list-like
        The window function to use for the filter.

        See `get_window` for details.

        Note that the window used here should be non-negative.

    n : int > 0
        the length of the filter

    slope : float
        The slope of the diagonal filter to produce

    angle : float or None
        If given, the slope parameter is ignored,
        and angle directly sets the orientation of the filter (in radians).
        Otherwise, angle is inferred as `arctan(slope)`.

    zero_mean : bool
        If True, a zero-mean filter is used.
        Otherwise, a non-negative averaging filter is used.

        This should be enabled if you want to enhance paths and suppress
        blocks.


    Returns
    -------
    kernel : np.ndarray, shape=[(m, m)]
        The 2-dimensional filter kernel


    Notes
    -----
    This function caches at level 10.
    """
    if angle is None:
        angle = np.arctan(slope)
    win = np.diag(get_window(window, n, fftbins=False))
    if not np.isclose(angle, np.pi / 4):
        win = scipy.ndimage.rotate(win, 45 - angle * 180 / np.pi, order=5, prefilter=False)
    np.clip(win, 0, None, out=win)
    win /= win.sum()
    if zero_mean:
        win -= win.mean()
    return win