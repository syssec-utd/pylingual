def fill_off_diagonal(x, radius, value=0):
    """Sets all cells of a matrix to a given ``value``
    if they lie outside a constraint region.
    In this case, the constraint region is the
    Sakoe-Chiba band which runs with a fixed ``radius``
    along the main diagonal.
    When ``x.shape[0] != x.shape[1]``, the radius will be
    expanded so that ``x[-1, -1] = 1`` always.

    ``x`` will be modified in place.

    Parameters
    ----------
    x : np.ndarray [shape=(N, M)]
        Input matrix, will be modified in place.
    radius : float
        The band radius (1/2 of the width) will be
        ``int(radius*min(x.shape))``.
    value : int
        ``x[n, m] = value`` when ``(n, m)`` lies outside the band.

    Examples
    --------
    >>> x = np.ones((8, 8))
    >>> librosa.util.fill_off_diagonal(x, 0.25)
    >>> x
    array([[1, 1, 0, 0, 0, 0, 0, 0],
           [1, 1, 1, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 0, 0, 0],
           [0, 0, 0, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0, 1, 1, 1],
           [0, 0, 0, 0, 0, 0, 1, 1]])
    >>> x = np.ones((8, 12))
    >>> librosa.util.fill_off_diagonal(x, 0.25)
    >>> x
    array([[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
           [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
           [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
           [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]])
    """
    (nx, ny) = x.shape
    radius = np.round(radius * np.min(x.shape))
    (nx, ny) = x.shape
    offset = np.abs(x.shape[0] - x.shape[1])
    if nx < ny:
        idx_u = np.triu_indices_from(x, k=radius + offset)
        idx_l = np.tril_indices_from(x, k=-radius)
    else:
        idx_u = np.triu_indices_from(x, k=radius)
        idx_l = np.tril_indices_from(x, k=-radius - offset)
    x[idx_u] = value
    x[idx_l] = value