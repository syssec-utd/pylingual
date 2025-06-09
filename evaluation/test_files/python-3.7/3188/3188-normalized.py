def describe(self, strings=True, virtual=True, selection=None):
    """Give a description of the DataFrame.

        >>> import vaex
        >>> df = vaex.example()[['x', 'y', 'z']]
        >>> df.describe()
                         x          y          z
        dtype      float64    float64    float64
        count       330000     330000     330000
        missing          0          0          0
        mean    -0.0671315 -0.0535899  0.0169582
        std        7.31746    7.78605    5.05521
        min       -128.294   -71.5524   -44.3342
        max        271.366    146.466    50.7185
        >>> df.describe(selection=df.x > 0)
                           x         y          z
        dtype        float64   float64    float64
        count         164060    164060     164060
        missing       165940    165940     165940
        mean         5.13572 -0.486786 -0.0868073
        std          5.18701   7.61621    5.02831
        min      1.51635e-05  -71.5524   -44.3342
        max          271.366   78.0724    40.2191

        :param bool strings: Describe string columns or not
        :param bool virtual: Describe virtual columns or not
        :param selection: Optional selection to use.
        :return: Pandas dataframe

        """
    import pandas as pd
    N = len(self)
    columns = {}
    for feature in self.get_column_names(strings=strings, virtual=virtual)[:]:
        dtype = str(self.dtype(feature)) if self.dtype(feature) != str else 'str'
        if self.dtype(feature) == str_type or self.dtype(feature).kind in ['S', 'U', 'O']:
            count = self.count(feature, selection=selection, delay=True)
            self.execute()
            count = count.get()
            columns[feature] = (dtype, count, N - count, '--', '--', '--', '--')
        else:
            count = self.count(feature, selection=selection, delay=True)
            mean = self.mean(feature, selection=selection, delay=True)
            std = self.std(feature, selection=selection, delay=True)
            minmax = self.minmax(feature, selection=selection, delay=True)
            self.execute()
            (count, mean, std, minmax) = (count.get(), mean.get(), std.get(), minmax.get())
            count = int(count)
            columns[feature] = (dtype, count, N - count, mean, std, minmax[0], minmax[1])
    return pd.DataFrame(data=columns, index=['dtype', 'count', 'missing', 'mean', 'std', 'min', 'max'])