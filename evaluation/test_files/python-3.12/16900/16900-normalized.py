def concatenate(self, arry, axis=0):
    """
        Join this array with another array.

        Paramters
        ---------
        arry : ndarray or BoltArrayLocal
            Another array to concatenate with

        axis : int, optional, default=0
            The axis along which arrays will be joined.

        Returns
        -------
        BoltArrayLocal
        """
    if isinstance(arry, ndarray):
        from bolt import concatenate
        return concatenate((self, arry), axis)
    else:
        raise ValueError('other must be local array, got %s' % type(arry))