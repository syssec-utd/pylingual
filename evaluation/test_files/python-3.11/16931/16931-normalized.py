def _getbasic(self, index):
    """
        Basic indexing (for slices or ints).
        """
    key_slices = index[0:self.split]
    value_slices = index[self.split:]

    def key_check(key):

        def inrange(k, s):
            if s.step > 0:
                return s.start <= k < s.stop
            else:
                return s.stop < k <= s.start

        def check(k, s):
            return inrange(k, s) and mod(k - s.start, s.step) == 0
        out = [check(k, s) for k, s in zip(key, key_slices)]
        return all(out)

    def key_func(key):
        return tuple([(k - s.start) / s.step for k, s in zip(key, key_slices)])
    filtered = self._rdd.filter(lambda kv: key_check(kv[0]))
    if self._split == self.ndim:
        rdd = filtered.map(lambda kv: (key_func(kv[0]), kv[1]))
    else:
        value_slices = [s if s.stop != -1 else slice(s.start, None, s.step) for s in value_slices]
        rdd = filtered.map(lambda kv: (key_func(kv[0]), kv[1][value_slices]))
    shape = tuple([int(ceil((s.stop - s.start) / float(s.step))) for s in index])
    split = self.split
    return (rdd, shape, split)