import numpy as np

def case_when(*args, default=np.nan, dtype=float):
    """

    SQL case when condition like for numpy array.

    Parameters
    ----------
    args: a numpy array
        A numpy array of lenght 2 * number of cases. With the first element of a pair is array of boolen and the second element of a pair is value if the condition is matched.
        
    default: int or float
        A value if there is none condition is matched.
    
    dtype: dtype
        dtype of the output array
        

    Examples
    --------
    arr = np.array([0, 2, 5, 3, 4, 10, 4])
    case_when(
        (np.isin(arr, [5, 10]), 5),
        (np.isin(arr, [2, 4, 6, 8, 10]), 2),
        (arr == 0, 0),
        default=-999   
    )

    Returns
    -------
    Numpy array of the same shape as inputted conditions with element assigned according to each case when condition.

	"""
    out_shape = args[0][0].shape
    arr_out = np.full(out_shape, np.nan)
    arr_non_default_mask = np.full(out_shape, False)
    for i in range(len(args)):
        assert out_shape == args[i][0].shape
        arr_out = np.where(np.isnan(arr_out) & args[i][0], args[i][1], arr_out)
        arr_non_default_mask = np.where(args[i][0], True, arr_non_default_mask)
    arr_out = np.where(arr_non_default_mask, arr_out, default)
    return arr_out.astype(dtype)

def fillna(in_arr, in_fillvalue):
    """

    Fill nan value in numpy array with fill in value(s).

    Parameters
    ----------
    in_arr: a numpy array
    in_fillvalue : a scalar or numpy array with the same shape of in_arr
        
        Returns
    -------
    out_arr: a numpy array that already filled

	"""
    out_arr = np.where(np.isnan(in_arr), in_fillvalue, in_arr)
    return out_arr

def get_last_n_digit(in_arr, nbr_digits=1):
    """
    Get N last digit(s) of the given array.
    """
    assert type(nbr_digits) == int
    assert nbr_digits >= 1
    assert nbr_digits <= 4
    divider = 10 ** nbr_digits
    out_arr = np.remainder(in_arr, divider).astype(int)
    return out_arr

def get_mod(in_arr, mod):
    """
    Get mod for given array
    """
    out_arr = np.remainder(in_arr, mod).astype(int)
    return out_arr