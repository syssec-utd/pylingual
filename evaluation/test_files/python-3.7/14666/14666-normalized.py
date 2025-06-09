def findmins(x, y):
    """ Function to find local minima.

    Parameters
    ----------
    x, y : array_like
        1D arrays of the independent (x) and dependent (y) variables.

    Returns
    -------
    array_like
        Array of points in x where y has a local minimum.
    """
    return x[np.r_[False, y[1:] < y[:-1]] & np.r_[y[:-1] < y[1:], False]]