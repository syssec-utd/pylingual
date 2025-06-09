def ablation_times(self):
    """
        Function for calculating the ablation time for each
        ablation.

        Returns
        -------
            dict of times for each ablation.
        """
    ats = {}
    for n in np.arange(self.n) + 1:
        t = self.Time[self.ns == n]
        ats[n - 1] = t.max() - t.min()
    return ats