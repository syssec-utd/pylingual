def transpose(self, *axes):
    """
        Transpose just the values of a BoltArraySpark, returning a
        new BoltArraySpark.

        Parameters
        ----------
        axes : tuple
             New proposed axes.
        """
    new = argpack(axes)
    old = range(self.ndim)
    istransposeable(new, old)
    if new == old:
        return self._barray

    def f(v):
        return v.transpose(new)
    newrdd = self._barray._rdd.mapValues(f)
    newshape = self._barray.keys.shape + tuple((self.shape[i] for i in new))
    return BoltArraySpark(newrdd, shape=newshape).__finalize__(self._barray)