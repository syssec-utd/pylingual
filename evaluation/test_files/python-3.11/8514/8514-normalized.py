def deinterleave(self, interleaved):
    """
        [xmin, ymin, xmax, ymax] => [xmin, xmax, ymin, ymax]

        >>> Index.deinterleave([0, 10, 1, 11])
        [0, 1, 10, 11]

        >>> Index.deinterleave([0, 1, 2, 10, 11, 12])
        [0, 10, 1, 11, 2, 12]

        """
    assert len(interleaved) % 2 == 0, 'must be a pairwise list'
    dimension = len(interleaved) // 2
    di = []
    for i in range(dimension):
        di.extend([interleaved[i], interleaved[i + dimension]])
    return di