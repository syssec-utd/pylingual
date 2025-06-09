def groupby(self, by=None, agg=None):
    """Return a :class:`GroupBy` or :class:`DataFrame` object when agg is not None

        Examples:

        >>> import vaex
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> x = np.random.randint(1, 5, 10)
        >>> y = x**2
        >>> df = vaex.from_arrays(x=x, y=y)
        >>> df.groupby(df.x, agg='count')
        #    x    y_count
        0    3          4
        1    4          2
        2    1          3
        3    2          1
        >>> df.groupby(df.x, agg=[vaex.agg.count('y'), vaex.agg.mean('y')])
        #    x    y_count    y_mean
        0    3          4         9
        1    4          2        16
        2    1          3         1
        3    2          1         4
        >>> df.groupby(df.x, agg={'z': [vaex.agg.count('y'), vaex.agg.mean('y')]})
        #    x    z_count    z_mean
        0    3          4         9
        1    4          2        16
        2    1          3         1
        3    2          1         4

        Example using datetime:

        >>> import vaex
        >>> import numpy as np
        >>> t = np.arange('2015-01-01', '2015-02-01', dtype=np.datetime64)
        >>> y = np.arange(len(t))
        >>> df = vaex.from_arrays(t=t, y=y)
        >>> df.groupby(vaex.BinnerTime.per_week(df.t)).agg({'y' : 'sum'})
        #  t                      y
        0  2015-01-01 00:00:00   21
        1  2015-01-08 00:00:00   70
        2  2015-01-15 00:00:00  119
        3  2015-01-22 00:00:00  168
        4  2015-01-29 00:00:00   87


        :param dict, list or agg agg: Aggregate operation in the form of a string, vaex.agg object, a dictionary
            where the keys indicate the target column names, and the values the operations, or the a list of aggregates.
            When not given, it will return the groupby object.
        :return: :class:`DataFrame` or :class:`GroupBy` object.
        """
    from .groupby import GroupBy
    groupby = GroupBy(self, by=by)
    if agg is None:
        return groupby
    else:
        return groupby.agg(agg)