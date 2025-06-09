def filter_threshold(self, analyte, threshold):
    """
        Apply threshold filter.

        Generates threshold filters for the given analytes above and below
        the specified threshold.

        Two filters are created with prefixes '_above' and '_below'.
            '_above' keeps all the data above the threshold.
            '_below' keeps all the data below the threshold.

        i.e. to select data below the threshold value, you should turn the
        '_above' filter off.

        Parameters
        ----------
        analyte : TYPE
            Description of `analyte`.
        threshold : TYPE
            Description of `threshold`.

        Returns
        -------
        None
        """
    params = locals()
    del params['self']
    (below, above) = filters.threshold(self.focus[analyte], threshold)
    setn = self.filt.maxset + 1
    self.filt.add(analyte + '_thresh_below', below, 'Keep below {:.3e} '.format(threshold) + analyte, params, setn=setn)
    self.filt.add(analyte + '_thresh_above', above, 'Keep above {:.3e} '.format(threshold) + analyte, params, setn=setn)