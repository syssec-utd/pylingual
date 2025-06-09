def tick(self, index, length):
    """
        Add tick marks in order of axes by width
        APIPARAM: chxtc     <axis index>,<length of tick mark>
        """
    assert int(length) <= 25, 'Width cannot be more than 25'
    self.data['ticks'].append('%s,%d' % (index, length))
    return self.parent