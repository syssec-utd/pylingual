def add_virtual_columns_cartesian_to_polar(self, x='x', y='y', radius_out='r_polar', azimuth_out='phi_polar', propagate_uncertainties=False, radians=False):
    """Convert cartesian to polar coordinates

        :param x: expression for x
        :param y: expression for y
        :param radius_out: name for the virtual column for the radius
        :param azimuth_out: name for the virtual column for the azimuth angle
        :param propagate_uncertainties: {propagate_uncertainties}
        :param radians: if True, azimuth is in radians, defaults to degrees
        :return:
        """
    x = self[x]
    y = self[y]
    if radians:
        to_degrees = ''
    else:
        to_degrees = '*180/pi'
    r = np.sqrt(x ** 2 + y ** 2)
    self[radius_out] = r
    phi = np.arctan2(y, x)
    if not radians:
        phi = phi * 180 / np.pi
    self[azimuth_out] = phi
    if propagate_uncertainties:
        self.propagate_uncertainties([self[radius_out], self[azimuth_out]])