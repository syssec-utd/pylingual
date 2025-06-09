def dt_day_name(x):
    """Returns the day names of a datetime sample in English.

    :returns: an expression containing the day names extracted from a datetime column.

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

    >>> df.date.dt.day_name
    Expression = dt_day_name(date)
    Length: 3 dtype: str (expression)
    ---------------------------------
    0    Monday
    1  Thursday
    2  Thursday
    """
    import pandas as pd
    return pd.Series(_pandas_dt_fix(x)).dt.day_name().values.astype(str)