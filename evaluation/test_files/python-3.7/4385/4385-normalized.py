def _funm_svd(a, func):
    """Apply real scalar function to singular values of a matrix.

    Args:
        a (array_like): (N, N) Matrix at which to evaluate the function.
        func (callable): Callable object that evaluates a scalar function f.

    Returns:
        ndarray: funm (N, N) Value of the matrix function specified by func
        evaluated at `A`.
    """
    (U, s, Vh) = la.svd(a, lapack_driver='gesvd')
    S = np.diag(func(s))
    return U.dot(S).dot(Vh)