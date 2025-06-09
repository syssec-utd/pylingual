def correct_spectral_interference(self, target_analyte, source_analyte, f):
    """
        Correct spectral interference.

        Subtract interference counts from target_analyte, based on the
        intensity of a source_analayte and a known fractional contribution (f).

        Correction takes the form:
        target_analyte -= source_analyte * f

        Only operates on background-corrected data ('bkgsub'). 
        
        To undo a correction,
        rerun `self.bkg_subtract()`.

        Parameters
        ----------
        target_analyte : str
            The name of the analyte to modify.
        source_analyte : str
            The name of the analyte to base the correction on.
        f : float
            The fraction of the intensity of the source_analyte to
            subtract from the target_analyte. Correction is:
            target_analyte - source_analyte * f

        Returns
        -------
        None
        """
    if target_analyte not in self.analytes:
        raise ValueError('target_analyte: {:} not in available analytes ({:})'.format(target_analyte, ', '.join(self.analytes)))
    if source_analyte not in self.analytes:
        raise ValueError('source_analyte: {:} not in available analytes ({:})'.format(source_analyte, ', '.join(self.analytes)))
    self.data['bkgsub'][target_analyte] -= self.data['bkgsub'][source_analyte] * f