def _is_in_max_difference(value_1, value_2, max_difference):
    """ Helper function to determine the difference of two values that can be np.uints. Works in python and numba mode.
    Circumvents numba bug #1653
    """
    if value_1 <= value_2:
        return value_2 - value_1 <= max_difference
    return value_1 - value_2 <= max_difference