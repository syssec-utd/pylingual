import numpy as np
import ctypes
from ._cubature import cubature as _cython_cubature
from ._cubature import cubature_raw_callback as _cython_cubature_raw_callback
__all__ = ['ERROR_INDIVIDUAL', 'ERROR_PAIRED', 'ERROR_L2', 'ERROR_L1', 'ERROR_LINF', 'cubature']
ERROR_INDIVIDUAL = 0
ERROR_PAIRED = 1
ERROR_L2 = 2
ERROR_L1 = 3
ERROR_LINF = 4
_call_map = {('h', True): 'hcubature_v', ('h', False): 'hcubature', ('p', True): 'pcubature_v', ('p', False): 'pcubature'}

def cubature(func, ndim, fdim, xmin, xmax, args=tuple(), kwargs=dict(), abserr=1e-08, relerr=1e-08, norm=ERROR_INDIVIDUAL, maxEval=0, adaptive='h', vectorized=False):
    """Numerical-integration using the cubature method.

    Parameters
    ----------
    func : callable
        If ``vectorized=False`` the callable must have the form:
            ``f(x_array, *args, **kwargs)``

            where:

            - `x_array` in an array containing the `ndim` variables
               being integrated
            - `args` is a tuple containing any other arguments
              required by the function
            - `kwargs` is a dict containing any keyword arguments
              required by the function
            - the function must return a 1-D `np.ndarray` object
            - example 1, vector valued function::

                  fdim = 3
                  def func(x_array, *args, **kwargs):
                      # note that here ndim=2 (2 variables)
                      x, y = x_array
                      return np.array([x**2-y**2, x*y, x*y**2])

            - example 2, scalar function::

                  fdim = 1
                  def func(x_array, *args, **kwargs):
                      # note that here ndim=2 (2 variables)
                      x, y = x_array
                      return x**2-y**2

        If ``vectorized=True`` the function must have the form:
            ``f(x_array, *args, **kwargs)``

            where:

            - `x_array` has ``shape=(npt, ndim)``
            - `args` is a tuple containing any other arguments
              required by the function
            - `kwargs` is a dict containing any keyword arguments
              required by the function
            - example 1, vector valued function::

                  # function that returns a vector with 3 values
                  fdim = 3
                  def func(x_array, *args, **kwargs):
                      # note that here ndim=2 (2 variables)
                      x = x_array[:, 0]
                      y = x_array[:, 1]
                      npt = x_array.shape[0]
                      out = np.zeros((npt, fdim))
                      out[:, 0] = x**2 - y**2
                      out[:, 1] = x*y
                      out[:, 2] = x*y**2
                      return out

            - example 2, scalar function::

                  fdim = 1
                  def func(x_array, *args, **kwargs):
                      # note that here ndim=3 (3 variables)
                      x = x_array[:, 0]
                      y = x_array[:, 1]
                      z = x_array[:, 2]
                      return x**2 + y**2 + z**2

        The results from both vectorized and non-vectorized examples
        above should be the same, but the vectorized implementation
        is much faster since it will take advantage of NumPy's vectorization
        capabilities.
    ndim : integer
        Number dimensions or number of variables being integrated.
    fdim : integer
        Length of the output vector given by `func`. It should be `1` if the
        function returns a scalar.
    xmin : array-like
        A 1-D array carring the minimum integration limit for each
        variable being integrated. It must be have:
        ``xmin.shape[0]=ndim``.
    xmax : array-like
        A 1-D array carring the maximum integration limit for each
        variable being integrated. It must be have:
        ``xmax.shape[0]=ndim``.
    args : tuple or list, optional
        Contains the extra arguments required by `func`.
    kwargs : dict-like, optional
        Contains the extra keyword arguments passed to `func`.
    adaptive : string, optional
        The adaptive scheme used along the adaptive integration:

        - 'h' means 'h-adaptive', where the domain is partitioned
        - 'p' means 'p-adaptive', where the order of the integration rule is
          increased

        The 'p-adaptive' scheme is often better for smoth functions in
        low dimensions.
    abserr : double, optional
        Integration stops when estimated absolute error is below this threshold
    relerr : double, optional
        Integration stops when estimated error in integral value is below this
        threshold
    norm : integer, optional
        Specifies the norm that is used to measure the error and
        determine convergence properties (irrelevant for
        single-valued functions).
        The `norm` argument takes one of the values:

        - ERROR_INDIVIDUAL: convergence is achieved only when each
            integrand individually satisfies the requested error
            tolerances;
        - ERROR_PAIRED: like ERROR_INDIVIDUAL, except that the
            integrands are grouped into consecutive pairs, with the error
            tolerance applied in a L2 sense to each pair. This option is
            mainly useful for integrating vectors of complex numbers,
            where each consecutive pair of real integrans is the real
            and imaginary parts of a single complex integrand, and you
            only care about the error in the complex plane rather than
            the error in the real and imaginary parts separately;
        - ERROR_L2
        - ERROR_L1
        - ERROR_LINF
            the absolute error is measured as |e| and the relative error
            as |err|/|val|, where |...| is the L1, L2, or L-infinity
            norm, respectively.  (|x| in the L1 norm is the sum of the
            absolute values of the components, in the L2 norm is the
            root mean square of the components, and in the L-infinity
            norm is the maximum absolute value of the components).

    maxEval : integer, optional
        The maximum number of function evaluations.
    vectorized : boolean, optional
        If ``vectorized=True`` the integration points are passed to the
        integrand function as an array of points, allowing parallel
        evaluation of different points.

    Returns
    -------
    val : numpy.ndarray
        The 1-D array of length ``fdim`` with the computed integral values
    err : numpy.ndarray
        The 1-D array of length ``fdim`` with the estimated errors. For
        smooth functions this estimate is usually conservative (see the
        results from the ``test_cubature.py`` script.

    Notes
    -----
    * The supplied function must return a 1-D ``np.ndarray`` object,
      even for single-valued functions

    References
    ----------
    .. [1] `Cubature (Multi-dimensional integration)
           <http://ab-initio.mit.edu/wiki/index.php/Cubature>`_.

    Examples
    --------

    >>> # Volume of a sphere:
    >>> import numpy as np
    >>> from cubature import cubature

    >>> def integrand_sphere(x_array, *args):
    >>>     r, theta, phi = x_array
    >>>     return np.array([r**2*sin(phi)])

    >>> ndim = 3
    >>> fdim = 1
    >>> radius = 1.
    >>> xmin = np.array([0, 0, 0])
    >>> xmax = np.array([radius, 2*pi, pi])
    >>> val, err = cubature(integrand_sphere, ndim, fdim, xmin, xmax)

    """
    xmin = np.asarray(xmin)
    xmax = np.asarray(xmax)
    try:
        assert xmin.shape[0] == ndim
    except:
        raise ValueError('xmin.shape[0] is not equal ndim')
    try:
        assert xmax.shape[0] == ndim
    except:
        raise ValueError('xmax.shape[0] is not equal ndim')
    use_raw_callback = isinstance(func, ctypes._CFuncPtr)
    if not use_raw_callback:
        if not vectorized:
            out = func(np.ones(ndim) * xmin, *args, **kwargs)
            try:
                if isinstance(out, float) or isinstance(out, int):
                    out = np.array([out])
                assert out.shape[0] == fdim
            except:
                raise ValueError('Length of func ouptut vector is different than fdim')
        else:
            out = func(np.ones((7, ndim)) * xmin, *args, **kwargs)
            if fdim > 1:
                try:
                    assert out.shape[0] == 7
                    assert out.shape[1] == fdim
                except:
                    raise ValueError('Output vector does not have shape=(:, fdim)')
            else:
                try:
                    assert out.ndim == 1
                    assert out.shape[0] == 7
                except:
                    raise ValueError('Output vector does not return a valid array')
    method = _call_map.get((adaptive, vectorized), None)
    if method is None:
        s = 'unknown combination of adaptive (`{!r}`) and vectorized (`{!r}`).'
        s = s.format(adaptive, vectorized)
        raise ValueError(s)
    elif use_raw_callback:
        (val, err) = _cython_cubature_raw_callback(func, ndim, fdim, xmin, xmax, method, abserr, relerr, norm, maxEval, args=args, kwargs=kwargs)
    else:
        (val, err) = _cython_cubature(func, ndim, fdim, xmin, xmax, method, abserr, relerr, norm, maxEval, args=args, kwargs=kwargs)
    return (val, err)