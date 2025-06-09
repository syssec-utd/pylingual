def optimal_partitions(sizes, counts, num_part):
    """Compute the optimal partitions given a distribution of set sizes.

    Args:
        sizes (numpy.array): The complete domain of set sizes in ascending
            order.
        counts (numpy.array): The frequencies of all set sizes in the same
            order as `sizes`.
        num_part (int): The number of partitions to create.

    Returns:
        list: A list of partitions in the form of `(lower, upper)` tuples,
            where `lower` and `upper` are lower and upper bound (inclusive)
            set sizes of each partition.
    """
    if num_part < 2:
        return [(sizes[0], sizes[-1])]
    if num_part >= len(sizes):
        partitions = [(x, x) for x in sizes]
        return partitions
    nfps = _compute_nfps_real(counts, sizes)
    (partitions, _, _) = _compute_best_partitions(num_part, sizes, nfps)
    return partitions