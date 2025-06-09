def set_Tc(self, Tc, T=None):
    """
        initialize the merger model with a coalescent time

        Args:
            - Tc:   a float or an iterable, if iterable another argument T of same shape is required
            - T:    an array like of same shape as Tc that specifies the time pivots corresponding to Tc
        Returns:
            - None
        """
    if isinstance(Tc, Iterable):
        if len(Tc) == len(T):
            x = np.concatenate(([-ttconf.BIG_NUMBER], T, [ttconf.BIG_NUMBER]))
            y = np.concatenate(([Tc[0]], Tc, [Tc[-1]]))
            self.Tc = interp1d(x, y)
        else:
            self.logger('need Tc values and Timepoints of equal length', 2, warn=True)
            self.Tc = interp1d([-ttconf.BIG_NUMBER, ttconf.BIG_NUMBER], [1e-05, 1e-05])
    else:
        self.Tc = interp1d([-ttconf.BIG_NUMBER, ttconf.BIG_NUMBER], [Tc + ttconf.TINY_NUMBER, Tc + ttconf.TINY_NUMBER])
    self.calc_integral_merger_rate()