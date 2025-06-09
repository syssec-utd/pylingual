def add_virtual_columns_cartesian_to_spherical(self, x='x', y='y', z='z', alpha='l', delta='b', distance='distance', radians=False, center=None, center_name='solar_position'):
    """Convert cartesian to spherical coordinates.



        :param x:
        :param y:
        :param z:
        :param alpha:
        :param delta: name for polar angle, ranges from -90 to 90 (or -pi to pi when radians is True).
        :param distance:
        :param radians:
        :param center:
        :param center_name:
        :return:
        """
    transform = '' if radians else '*180./pi'
    if center is not None:
        self.add_variable(center_name, center)
    if center is not None and center[0] != 0:
        x = '({x} - {center_name}[0])'.format(**locals())
    if center is not None and center[1] != 0:
        y = '({y} - {center_name}[1])'.format(**locals())
    if center is not None and center[2] != 0:
        z = '({z} - {center_name}[2])'.format(**locals())
    self.add_virtual_column(distance, 'sqrt({x}**2 + {y}**2 + {z}**2)'.format(**locals()))
    self.add_virtual_column(alpha, 'arctan2({y}, {x}){transform}'.format(**locals()))
    self.add_virtual_column(delta, '(-arccos({z}/{distance})+pi/2){transform}'.format(**locals()))