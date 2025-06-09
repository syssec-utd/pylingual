def cluster_meanshift(data, bandwidth=None, bin_seeding=False, **kwargs):
    """
    Identify clusters using Meanshift algorithm.

    Parameters
    ----------
    data : array_like
        array of size [n_samples, n_features].
    bandwidth : float or None
        If None, bandwidth is estimated automatically using
        sklean.cluster.estimate_bandwidth
    bin_seeding : bool
        Setting this option to True will speed up the algorithm.
        See sklearn documentation for full description.

    Returns
    -------
    dict
        boolean array for each identified cluster.
    """
    if bandwidth is None:
        bandwidth = cl.estimate_bandwidth(data)
    ms = cl.MeanShift(bandwidth=bandwidth, bin_seeding=bin_seeding, **kwargs)
    ms.fit(data)
    labels = ms.labels_
    return (labels, [np.nan])