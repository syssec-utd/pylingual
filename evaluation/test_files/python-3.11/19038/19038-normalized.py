def get_random_available(self, max_iter=10000):
    """
        get a random key out of the first max_iter rows
        """
    c = 1
    keeper = None
    for row in self._available.get_range(row_count=max_iter, read_consistency_level=pycassa.ConsistencyLevel.ALL):
        logger.debug('considering %r' % (row,))
        if random.random() < 1 / c:
            keeper = row[0]
        if c == max_iter:
            break
        c += 1
    return keeper