def _align(self, axes, key_shape=None):
    """
        Align local bolt array so that axes for iteration are in the keys.

        This operation is applied before most functional operators.
        It ensures that the specified axes are valid, and might transpose/reshape
        the underlying array so that the functional operators can be applied
        over the correct records.

        Parameters
        ----------
        axes: tuple[int]
            One or more axes that will be iterated over by a functional operator

        Returns
        -------
        BoltArrayLocal
        """
    inshape(self.shape, axes)
    remaining = [dim for dim in range(len(self.shape)) if dim not in axes]
    key_shape = key_shape if key_shape else [self.shape[axis] for axis in axes]
    remaining_shape = [self.shape[axis] for axis in remaining]
    linearized_shape = [prod(key_shape)] + remaining_shape
    transpose_order = axes + remaining
    reshaped = self.transpose(*transpose_order).reshape(*linearized_shape)
    return reshaped