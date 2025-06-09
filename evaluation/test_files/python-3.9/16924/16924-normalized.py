def mean(self, axis=None, keepdims=False):
    """
        Return the mean of the array over the given axis.

        Parameters
        ----------
        axis : tuple or int, optional, default=None
            Axis to compute statistic over, if None
            will compute over all axes

        keepdims : boolean, optional, default=False
            Keep axis remaining after operation with size 1.
        """
    return self._stat(axis, name='mean', keepdims=keepdims)