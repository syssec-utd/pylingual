def gradient_histogram(self, analytes=None, win=15, filt=False, bins=None, samples=None, subset=None, recalc=True, ncol=4):
    """
        Plot a histogram of the gradients in all samples.

        Parameters
        ----------
        filt : str, dict or bool
            Either logical filter expression contained in a str,
            a dict of expressions specifying the filter string to
            use for each analyte or a boolean. Passed to `grab_filt`.
        bins : None or array-like
            The bins to use in the histogram
        samples : str or list
            which samples to get
        subset : str or int
            which subset to get
        recalc : bool
            Whether to re-calculate the gradients, or use existing gradients.

        Returns
        -------
        fig, ax
        """
    if analytes is None:
        analytes = [a for a in self.analytes if self.internal_standard not in a]
    if not hasattr(self, 'gradients'):
        self.gradients = Bunch()
    ncol = int(ncol)
    n = len(analytes)
    nrow = plot.calc_nrow(n, ncol)
    if samples is not None:
        subset = self.make_subset(samples)
    samples = self._get_samples(subset)
    self.get_gradients(analytes=analytes, win=win, filt=filt, subset=subset, recalc=recalc)
    fig, axs = plt.subplots(nrow, ncol, figsize=[3.0 * ncol, 2.5 * nrow])
    if not isinstance(axs, np.ndarray):
        axs = [axs]
    i = 0
    for a, ax in zip(analytes, axs.flatten()):
        d = nominal_values(self.gradients[a])
        d = d[~np.isnan(d)]
        m, u = unitpicker(d, focus_stage=self.focus_stage, denominator=self.internal_standard)
        if bins is None:
            ibins = np.linspace(*np.percentile(d * m, [1, 99]), 50)
        else:
            ibins = bins
        ax.hist(d * m, bins=ibins, color=self.cmaps[a])
        ax.axvline(0, ls='dashed', lw=1, c=(0, 0, 0, 0.7))
        ax.set_title(a, loc='left')
        if ax.is_first_col():
            ax.set_ylabel('N')
        ax.set_xlabel(u + '/s')
        i += 1
    if i < ncol * nrow:
        for ax in axs.flatten()[i:]:
            ax.set_visible(False)
    fig.tight_layout()
    return (fig, axs)