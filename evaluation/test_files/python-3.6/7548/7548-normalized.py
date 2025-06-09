def get_keys(self, start, count=1, step=1, iterations=1):
    """
        Generates and returns one or more keys at the specified
        index(es).

        This is a one-time operation; if you want to create lots of keys
        across multiple contexts, consider invoking
        :py:meth:`create_iterator` and sharing the resulting generator
        object instead.

        Warning: This method may take awhile to run if the starting
        index and/or the number of requested keys is a large number!

        :param start:
            Starting index.
            Must be >= 0.

        :param count:
            Number of keys to generate.
            Must be > 0.

        :param step:
            Number of indexes to advance after each key.
            This may be any non-zero (positive or negative) integer.

        :param iterations:
            Number of transform iterations to apply to each key, also
            known as security level.
            Must be >= 1.

            Increasing this value makes key generation slower, but more
            resistant to brute-forcing.

        :return:
            Always returns a list, even if only one key is generated.

            The returned list will contain ``count`` keys, except when
            ``step * count < start`` (only applies when ``step`` is
            negative).
        """
    if count < 1:
        raise with_context(exc=ValueError('``count`` must be positive.'), context={'start': start, 'count': count, 'step': step, 'iterations': iterations})
    if not step:
        raise with_context(exc=ValueError('``step`` must not be zero.'), context={'start': start, 'count': count, 'step': step, 'iterations': iterations})
    iterator = self.create_iterator(start, step, iterations)
    keys = []
    for _ in range(count):
        try:
            next_key = next(iterator)
        except StopIteration:
            break
        else:
            keys.append(next_key)
    return keys