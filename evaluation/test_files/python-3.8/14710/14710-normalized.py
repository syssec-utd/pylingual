def gplot(self, analytes=None, win=25, figsize=[10, 4], ranges=False, focus_stage=None, ax=None, recalc=True):
    """
        Plot analytes gradients as a function of Time.

        Parameters
        ----------
        analytes : array_like
            list of strings containing names of analytes to plot.
            None = all analytes.
        win : int
            The window over which to calculate the rolling gradient.
        figsize : tuple
            size of final figure.
        ranges : bool
            show signal/background regions.

        Returns
        -------
        figure, axis
        """
    if type(analytes) is str:
        analytes = [analytes]
    if analytes is None:
        analytes = self.analytes
    if focus_stage is None:
        focus_stage = self.focus_stage
    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0.1, 0.12, 0.77, 0.8])
        ret = True
    else:
        fig = ax.figure
        ret = False
    x = self.Time
    if recalc or not self.grads_calced:
        self.grads = calc_grads(x, self.data[focus_stage], analytes, win)
        self.grads_calce = True
    for a in analytes:
        ax.plot(x, self.grads[a], color=self.cmap[a], label=a)
    if ranges:
        for lims in self.bkgrng:
            ax.axvspan(*lims, color='k', alpha=0.1, zorder=-1)
        for lims in self.sigrng:
            ax.axvspan(*lims, color='r', alpha=0.1, zorder=-1)
    ax.text(0.01, 0.99, self.sample + ' : ' + self.focus_stage + ' : gradient', transform=ax.transAxes, ha='left', va='top')
    ax.set_xlabel('Time (s)')
    ax.set_xlim(np.nanmin(x), np.nanmax(x))
    ud = {'rawdata': 'counts/s', 'despiked': 'counts/s', 'bkgsub': 'background corrected counts/s', 'ratios': 'counts/{:s} count/s', 'calibrated': 'mol/mol {:s}/s'}
    if focus_stage in ['ratios', 'calibrated']:
        ud[focus_stage] = ud[focus_stage].format(self.internal_standard)
    ax.set_ylabel(ud[focus_stage])

    def yfmt(x, p):
        return '{:.0e}'.format(x)
    ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(yfmt))
    ax.legend(bbox_to_anchor=(1.15, 1))
    ax.axhline(0, color='k', lw=1, ls='dashed', alpha=0.5)
    if ret:
        return (fig, ax)