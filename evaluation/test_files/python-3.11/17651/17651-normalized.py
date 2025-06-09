def trisolve(dl, d, du, b, inplace=False):
    """
    The tridiagonal matrix (Thomas) algorithm for solving tridiagonal systems
    of equations:

        a_{i}x_{i-1} + b_{i}x_{i} + c_{i}x_{i+1} = y_{i}

    in matrix form:
        Mx = b

    TDMA is O(n), whereas standard Gaussian elimination is O(n^3).

    Arguments:
    -----------
        dl: (n - 1,) vector
            the lower diagonal of M
        d: (n,) vector
            the main diagonal of M
        du: (n - 1,) vector
            the upper diagonal of M
        b: (n,) vector
            the result of Mx
        inplace:
            if True, and if d and b are both float64 vectors, they will be
            modified in place (may be faster)

    Returns:
    -----------
        x: (n,) vector
            the solution to Mx = b

    References:
    -----------
    http://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm
    http://www.netlib.org/lapack/explore-html/d1/db3/dgtsv_8f.html
    """
    if dl.shape[0] != du.shape[0] or d.shape[0] != dl.shape[0] + 1 or d.shape[0] != b.shape[0]:
        raise ValueError('Invalid diagonal shapes')
    bshape_in = b.shape
    rtype = np.result_type(dl, d, du, b)
    if not inplace:
        dl = np.array(dl, dtype=rtype, copy=True, order='F')
        d = np.array(d, dtype=rtype, copy=True, order='F')
        du = np.array(du, dtype=rtype, copy=True, order='F')
        b = np.array(b, dtype=rtype, copy=True, order='F')
    dl, d, du, b = (np.array(v, dtype=rtype, copy=False, order='F') for v in (dl, d, du, b))
    _lapack_trisolve(dl, d, du, b, rtype)
    return b.reshape(bshape_in)