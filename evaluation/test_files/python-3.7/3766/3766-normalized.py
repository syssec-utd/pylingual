def outer(vector1, vector2=None):
    """
    Construct the outer product of two vectors.

    The second vector argument is optional, if absent the projector
    of the first vector will be returned.

    Args:
        vector1 (ndarray): the first vector.
        vector2 (ndarray): the (optional) second vector.

    Returns:
        np.array: The matrix |v1><v2|.

    """
    if vector2 is None:
        vector2 = np.array(vector1).conj()
    else:
        vector2 = np.array(vector2).conj()
    return np.outer(vector1, vector2)