def dt_year(x):
    """Extracts the year out of a datetime sample.

    :returns: an expression containing the year extracted from a datetime column.

    Example:

    >>> import vaex
    >>> import numpy as np
    >>> date = np.array(['2009-10-12T03:31:00', '2016-02-11T10:17:34', '2015-11-12T11:34:22'], dtype=np.datetime64)
    >>> df = vaex.from_arrays(date=date)
    >>> df
      #  date
      0  2009-10-12 03:31:00
      1  2016-02-11 10:17:34
      2  2015-11-12 11:34:22

    >>> df.date.dt.year
    Expression = dt_year(date)
    Length: 3 dtype: int64 (expression)
    -----------------------------------
    0  2009
    1  2016
    2  2015
    """
    import pandas as pd
    return pd.Series(x).dt.year.values