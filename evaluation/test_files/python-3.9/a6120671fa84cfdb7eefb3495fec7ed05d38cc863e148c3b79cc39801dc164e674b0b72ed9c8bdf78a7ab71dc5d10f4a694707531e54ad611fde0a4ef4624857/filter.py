__all__ = ['savgol_filter', 'detrend']
__dataset_methods__ = __all__
import scipy.signal
'wrappers of scipy.signal filters, '

def savgol_filter(dataset, window_length=5, polyorder=0, deriv=0, delta=1.0, mode='interp', cval=0.0, **kwargs):
    """
    Apply a Savitzky-Golay filter to a NDDataset.

    Wrapper of scpy.signal.savgol(). If dataset has dimension greater than 1,
    dim determines the axis along which the filter is applied.

    Parameters
    ----------
    dataset : `NDDataset`
        The dataset to be filtered. If dataset.data is not a single or double precision
        floating point array, it will be converted to type numpy.float64 before
        filtering.
    window_length : int
        The length of the filter window (i.e. the number of coefficients).
        window_length must be a positive odd integer.
    polyorder : int
        The order of the polynomial used to fit the NDDataset. `polyorder` must be less
        than window_length.
    deriv : int, optional
        The order of the derivative to compute. This must be a non-negative integer.
        The default is 0, which means to filter the data without differentiating.
    delta : float, optional
        The spacing of the samples to which the filter will be applied. This is only
        used if deriv > 0. Default is 1.0.
    mode : str, optional
        Must be ‘mirror’, ‘constant’, ‘nearest’, ‘wrap’ or ‘interp’. This determines
        the type of extension to use for
        the padded signal to which the filter is applied. When mode is ‘constant’,
        the padding value is given by cval.
        See :py:scipy.signal.savgol_filter: for more details on ‘mirror’, ‘constant’,
        ‘wrap’, and ‘nearest’.
        When the ‘interp’ mode is selected (the default), no extension is used.
        Instead, a degree polyorder polynomial is fit to the last window_length values
        of the edges, and this polynomial is used to evaluate the
        last window_length // 2 output values.
    cval : scalar, optional
        Value to fill past the edges of the input if mode is ‘constant’. Default is 0.0.
    **kwargs
        Optional keyword parameters (see Other Parameters).

    Returns
    -------
    NDDataset
        The filtered data with same shape as x. data units are removed when deriv > 1.

    Other Parameters
    ----------------
    dim : str or int, optional, default='x'
        Specify on which dimension to apply this method. If `dim` is specified as an
        integer it is equivalent to the usual `axis` numpy parameter.
    inplace : bool, optional, default=False
        True if we make the transform inplace.  If False, the function return a new
        object.

    Notes
    -----
    Even spacing of the axis coordinates is NOT checked. Be aware that Savitzky-Golay
    algorithm is based on indexes, not on coordinates.

    Details on the `mode` options:

    * `mirror` :
      Repeats the values at the edges in reverse order.  The value
      closest to the edge is not included.
    * `nearest` :
      The extension contains the nearest input value.
    * `constant` :
      The extension contains the value given by the `cval` argument.
    * `wrap` :
      The extension contains the values from the other end of the array.

    For example, if the input is [1, 2, 3, 4, 5, 6, 7, 8], and
    `window_length` is 7, the following shows the extended data for
    the various `mode` options (assuming `cval` is 0)

    +------------+----------+------------------------+---------+
    | Mode       |   Ext    |         Input          |   Ext   |
    +============+==========+========================+=========+
    | 'mirror'   | 4  3  2  | 1  2  3  4  5  6  7  8 | 7  6  5 |
    +------------+----------+------------------------+---------+
    | 'nearest'  | 1  1  1  | 1  2  3  4  5  6  7  8 | 8  8  8 |
    +------------+----------+------------------------+---------+
    | 'constant' | 0  0  0  | 1  2  3  4  5  6  7  8 | 0  0  0 |
    +------------+----------+------------------------+---------+
    | 'wrap'     | 6  7  8  | 1  2  3  4  5  6  7  8 | 1  2  3 |
    +------------+----------+------------------------+---------+


    See Also
    ---------
    smooth : Smooth the data using a window with requested size.

    Examples
    --------

    >>> dataset = scp.read('irdata/nh4y-activation.spg')
    >>> dataset.savgol_filter(window_length=5, polyorder=0)
    NDDataset: [float64] a.u. (shape: (y:55, x:5549))
    """
    new = dataset.copy() if not kwargs.pop('inplace', False) else dataset
    is_ndarray = False
    axis = kwargs.pop('dim', kwargs.pop('axis', -1))
    if hasattr(new, 'get_axis'):
        (axis, dim) = new.get_axis(axis, negative_axis=True)
        data = new.data
    else:
        is_ndarray = True
        data = new
    data = scipy.signal.savgol_filter(data, window_length, polyorder, deriv, delta, axis, mode, cval)
    if not is_ndarray:
        if deriv != 0 and dataset.coord(dim).reversed:
            data = data * (-1) ** deriv
        new.data = data
    else:
        new = data
    if not is_ndarray:
        new.history = f'savgol_filter applied (window_length={window_length}, polyorder={polyorder}, deriv={deriv}, delta={delta}, mode={mode}, cval={cval}'
    return new

def detrend(dataset, type='linear', bp=0, **kwargs):
    """
    Remove linear trend along dim from dataset.

    Wrapper of scpy.signal.detrend().

    Parameters
    ----------
    dataset :  `NDDataset`
        The input data.
    type : str among ['linear', 'constant'}, optional, default='linear'
        The type of detrending. If `type == 'linear'` (default),
        the result of a linear least-squares fit to `data` is subtracted from `data` .
        If `type == 'constant'` , only the mean of `data` is subtracted.
    bp : array_like of ints, optional
        A sequence of break points. If given, an individual linear fit is
        performed for each part of `data` between two break points.
        Break points are specified as indices into `data` .
    **kwargs
        Optional keyword parameters (see Other Parameters).

    Returns
    -------
    detrended
        The detrended `NDDataset` .

    Other Parameters
    ----------------
    dim : str or int, optional, default='x'.
        Specify on which dimension to apply this method. If `dim` is specified as an
        integer it is equivalent to the usual `axis` numpy parameter.
    inplace : bool, optional, default=False.
        True if we make the transform inplace.  If False, the function return a new
        object

    See Also
    --------
    BaselineCorrection : Manual baseline correction.
    abs : Automatic baseline correction.
    autosub : Subtraction of reference.

    Examples
    --------

    >>> dataset = scp.read("irdata/nh4y-activation.spg")
    >>> dataset.detrend(type='constant')
    NDDataset: [float64] a.u. (shape: (y:55, x:5549))
    """
    if not kwargs.pop('inplace', False):
        new = dataset.copy()
    else:
        new = dataset
    is_ndarray = False
    axis = kwargs.pop('dim', kwargs.pop('axis', -1))
    if hasattr(new, 'get_axis'):
        (axis, dim) = new.get_axis(axis, negative_axis=True)
        data = new.data
    else:
        is_ndarray = True
        data = new
    data = scipy.signal.detrend(data, axis=axis, type=type, bp=bp)
    if is_ndarray:
        return data
    new.data = data
    return new