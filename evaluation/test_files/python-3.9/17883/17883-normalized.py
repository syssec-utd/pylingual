def from_array(array):
    """
    Export a numpy array to a blosc array.

    Arguments:
        array: The numpy array to compress to blosc array

    Returns:
        Bytes/String. A blosc compressed array
    """
    try:
        raw_data = blosc.pack_array(array)
    except Exception as e:
        raise ValueError('Could not compress data from array. {}'.format(e))
    return raw_data