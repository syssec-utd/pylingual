def pick_peaks(nc, L=16):
    """Obtain peaks from a novelty curve using an adaptive threshold."""
    offset = nc.mean() / 20.0
    nc = filters.gaussian_filter1d(nc, sigma=4)
    th = filters.median_filter(nc, size=L) + offset
    peaks = []
    for i in range(1, nc.shape[0] - 1):
        if nc[i - 1] < nc[i] and nc[i] > nc[i + 1]:
            if nc[i] > th[i]:
                peaks.append(i)
    return peaks