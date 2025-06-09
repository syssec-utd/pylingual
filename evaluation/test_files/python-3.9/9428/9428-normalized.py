def _homogeneity_filter(ls, window_size):
    """
    Takes `ls` (a list of 1s and 0s) and smoothes it so that adjacent values are more likely
    to be the same.

    :param ls:          A list of 1s and 0s to smooth.
    :param window_size: How large the smoothing kernel is.
    :returns:           A list of 1s and 0s, but smoother.
    """
    k = window_size
    i = k
    while i <= len(ls) - k:
        window = [ls[i + j] for j in range(k)]
        mode = 1 if sum(window) >= k / 2 else 0
        for j in range(k):
            ls[i + j] = mode
        i += k
    return ls