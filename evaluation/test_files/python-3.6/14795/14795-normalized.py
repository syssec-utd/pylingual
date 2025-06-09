def calc_window_mean_std(s, min_points, ind=None):
    """
    Apply fn to all contiguous regions in s that have at least min_points.
    """
    max_points = np.sum(~np.isnan(s))
    n_points = max_points - min_points
    mean = np.full((n_points, s.size), np.nan)
    std = np.full((n_points, s.size), np.nan)
    if ind is None:
        ind = ~np.isnan(s)
    else:
        ind = ind & ~np.isnan(s)
    s = s[ind]
    for (i, w) in enumerate(range(min_points, s.size)):
        r = rolling_window(s, w, pad=np.nan)
        mean[i, ind] = r.sum(1) / w
        std[i, ind] = (((r - mean[i, ind][:, np.newaxis]) ** 2).sum(1) / (w - 1)) ** 0.5
    return (mean, std)