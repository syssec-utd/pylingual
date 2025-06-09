def optimisation_plots(self, overlay_alpha=0.5, samples=None, subset=None, **kwargs):
    """
        Plot the result of signal_optimise.

        `signal_optimiser` must be run first, and the output
        stored in the `opt` attribute of the latools.D object.

        Parameters
        ----------
        d : latools.D object
            A latools data object.
        overlay_alpha : float
            The opacity of the threshold overlays. Between 0 and 1.
        **kwargs
            Passed to `tplot`
        """
    if samples is not None:
        subset = self.make_subset(samples)
    samples = self._get_samples(subset)
    outdir = self.report_dir + '/optimisation_plots/'
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    with self.pbar.set(total=len(samples), desc='Drawing Plots') as prog:
        for s in samples:
            figs = self.data[s].optimisation_plot(overlay_alpha, **kwargs)
            n = 1
            for f, _ in figs:
                if f is not None:
                    f.savefig(outdir + '/' + s + '_optim_{:.0f}.pdf'.format(n))
                    plt.close(f)
                n += 1
            prog.update()
    return