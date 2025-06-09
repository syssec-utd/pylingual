def dequantize(arr, min_val, max_val, levels, dtype=np.float64):
    """Dequantize an array.

    Args:
        arr (ndarray): Input array.
        min_val (scalar): Minimum value to be clipped.
        max_val (scalar): Maximum value to be clipped.
        levels (int): Quantization levels.
        dtype (np.type): The type of the dequantized array.

    Returns:
        tuple: Dequantized array.
    """
    if not (isinstance(levels, int) and levels > 1):
        raise ValueError('levels must be a positive integer, but got {}'.format(levels))
    if min_val >= max_val:
        raise ValueError('min_val ({}) must be smaller than max_val ({})'.format(min_val, max_val))
    dequantized_arr = (arr + 0.5).astype(dtype) * (max_val - min_val) / levels + min_val
    return dequantized_arr