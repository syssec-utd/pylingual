def from_csv(filename_or_buffer, copy_index=True, **kwargs):
    """Shortcut to read a csv file using pandas and convert to a DataFrame directly.

    :rtype: DataFrame
    """
    import pandas as pd
    return from_pandas(pd.read_csv(filename_or_buffer, **kwargs), copy_index=copy_index)