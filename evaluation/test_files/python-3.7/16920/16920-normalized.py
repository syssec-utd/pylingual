def map(self, func, axis=(0,), value_shape=None, dtype=None, with_keys=False):
    """
        Apply a function across an axis.

        Array will be aligned so that the desired set of axes
        are in the keys, which may incur a swap.

        Parameters
        ----------
        func : function
            Function of a single array to apply. If with_keys=True,
            function should be of a (tuple, array) pair.

        axis : tuple or int, optional, default=(0,)
            Axis or multiple axes to apply function along.

        value_shape : tuple, optional, default=None
            Known shape of values resulting from operation

        dtype: numpy.dtype, optional, default=None
            Known dtype of values resulting from operation

        with_keys : bool, optional, default=False
            Include keys as an argument to the function

        Returns
        -------
        BoltArraySpark
        """
    axis = tupleize(axis)
    swapped = self._align(axis)
    if with_keys:
        test_func = lambda x: func(((0,), x))
    else:
        test_func = func
    if value_shape is None or dtype is None:
        try:
            mapped = test_func(random.randn(*swapped.values.shape).astype(self.dtype))
        except Exception:
            first = swapped._rdd.first()
            if first:
                mapped = test_func(first[1])
        if value_shape is None:
            value_shape = mapped.shape
        if dtype is None:
            dtype = mapped.dtype
    shape = tuple([swapped._shape[ax] for ax in range(len(axis))]) + tupleize(value_shape)
    if with_keys:
        rdd = swapped._rdd.map(lambda kv: (kv[0], func(kv)))
    else:
        rdd = swapped._rdd.mapValues(func)

    def check(v):
        if len(v.shape) > 0 and v.shape != tupleize(value_shape):
            raise Exception('Map operation did not produce values of uniform shape.')
        return v
    rdd = rdd.mapValues(lambda v: check(v))
    return self._constructor(rdd, shape=shape, dtype=dtype, split=swapped.split).__finalize__(swapped)