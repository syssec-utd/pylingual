def map_clusters(self, size, sampled, clusters):
    """
        Translate cluster identity back to original data size.

        Parameters
        ----------
        size : int
            size of original dataset
        sampled : array-like
            integer array describing location of finite values
            in original data.
        clusters : array-like
            integer array of cluster identities

        Returns
        -------
        list of cluster identities the same length as original
        data. Where original data are non-finite, returns -2.

        """
    ids = np.zeros(size, dtype=int)
    ids[:] = -2
    ids[sampled] = clusters
    return ids