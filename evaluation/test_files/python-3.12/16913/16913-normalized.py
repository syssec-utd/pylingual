def getnumber(plan, shape):
    """
        Obtain number of chunks for the given dimensions and chunk sizes.

        Given a plan for the number of chunks along each dimension,
        calculate the number of chunks that this will lead to.

        Parameters
        ----------
        plan: tuple or array-like
            Size of chunks (in number of elements) along each dimensions.
            Length must be equal to the number of dimensions.

        shape : tuple
             Shape of array to be chunked.
        """
    nchunks = []
    for size, d in zip(plan, shape):
        nchunks.append(int(ceil(1.0 * d / size)))
    return nchunks