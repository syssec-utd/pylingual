def range(self, index, *args):
    """
        Set the range of each axis, one at a time
        args are of the form <start of range>,<end of range>,<interval>
        APIPARAM: chxr
        """
    self.data['ranges'].append('%s,%s' % (index, ','.join(map(smart_str, args))))
    return self.parent