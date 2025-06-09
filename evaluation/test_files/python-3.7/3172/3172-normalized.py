def add_column_healpix(self, name='healpix', longitude='ra', latitude='dec', degrees=True, healpix_order=12, nest=True):
    """Add a healpix (in memory) column based on a longitude and latitude

        :param name: Name of column
        :param longitude: longitude expression
        :param latitude: latitude expression  (astronomical convenction latitude=90 is north pole)
        :param degrees: If lon/lat are in degrees (default) or radians.
        :param healpix_order: healpix order, >= 0
        :param nest: Nested healpix (default) or ring.
        """
    import healpy as hp
    if degrees:
        scale = '*pi/180'
    else:
        scale = ''
    phi = self.evaluate('(%s)%s' % (longitude, scale))
    theta = self.evaluate('pi/2-(%s)%s' % (latitude, scale))
    hp_index = hp.ang2pix(hp.order2nside(healpix_order), theta, phi, nest=nest)
    self.add_column('healpix', hp_index)