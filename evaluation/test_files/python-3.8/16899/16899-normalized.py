def reduce(self, func, axis=0):
    """
        Reduce an array along an axis.

        Applies an associative/commutative function of two arguments
        cumulatively to all arrays along an axis. Array will be aligned
        so that the desired set of axes are in the keys, which may
        require a transpose/reshape.

        Parameters
        ----------
        func : function
            Function of two arrays that returns a single array

        axis : tuple or int, optional, default=(0,)
            Axis or multiple axes to reduce along.

        Returns
        -------
        BoltArrayLocal
        """
    axes = sorted(tupleize(axis))
    if isinstance(func, ufunc):
        inshape(self.shape, axes)
        reduced = func.reduce(self, axis=tuple(axes))
    else:
        reshaped = self._align(axes)
        reduced = reduce(func, reshaped)
    new_array = self._constructor(reduced)
    expected_shape = [self.shape[i] for i in range(len(self.shape)) if i not in axes]
    if new_array.shape != tuple(expected_shape):
        raise ValueError('reduce did not yield a BoltArray with valid dimensions')
    return new_array