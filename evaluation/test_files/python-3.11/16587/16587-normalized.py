def build_bbp(self, x, y, wave_const=550):
    """
        Builds the particle backscattering function  :math:`X(\\frac{550}{\\lambda})^Y`

        :param x: function coefficient
        :param y: order of the power function
        :param wave_const: wave constant default 550 (nm)
        :returns null:
        """
    lg.info('Building b_bp spectra')
    self.b_bp = x * (wave_const / self.wavelengths) ** y