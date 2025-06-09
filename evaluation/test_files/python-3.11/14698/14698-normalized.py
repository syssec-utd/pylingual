def correlation_plot(self, x_analyte, y_analyte, window=15, filt=True, recalc=False):
    """
        Plot the local correlation between two analytes.

        Parameters
        ----------
        x_analyte, y_analyte : str
            The names of the x and y analytes to correlate.
        window : int, None
            The rolling window used when calculating the correlation.
        filt : bool
            Whether or not to apply existing filters to the data before
            calculating this filter.
        recalc : bool
            If True, the correlation is re-calculated, even if it is already present.

        Returns
        -------
        fig, axs : figure and axes objects
        """
    label = '{:}_{:}_{:.0f}'.format(x_analyte, y_analyte, window)
    self.calc_correlation(x_analyte, y_analyte, window, filt, recalc)
    r, p = self.correlations[label]
    fig, axs = plt.subplots(3, 1, figsize=[7, 5], sharex=True)
    ax = axs[0]
    ax.plot(self.Time, nominal_values(self.focus[x_analyte]), color=self.cmap[x_analyte], label=x_analyte)
    ax.plot(self.Time, nominal_values(self.focus[y_analyte]), color=self.cmap[y_analyte], label=y_analyte)
    ax.set_yscale('log')
    ax.legend()
    ax.set_ylabel('Signals')
    ax = axs[1]
    ax.plot(self.Time, r)
    ax.set_ylabel('Pearson R')
    ax = axs[2]
    ax.plot(self.Time, p)
    ax.set_ylabel('pignificance Level (p)')
    fig.tight_layout()
    return (fig, axs)