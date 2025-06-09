def ones(shape, dtype=float64, order='C'):
    """
        Create a local bolt array of ones.

        Parameters
        ----------
        shape : tuple
            Dimensions of the desired array

        dtype : data-type, optional, default=float64
            The desired data-type for the array. (see numpy)

        order : {'C', 'F', 'A'}, optional, default='C'
            The order of the array. (see numpy)

        Returns
        -------
        BoltArrayLocal
        """
    from numpy import ones
    return ConstructLocal._wrap(ones, shape, dtype, order)