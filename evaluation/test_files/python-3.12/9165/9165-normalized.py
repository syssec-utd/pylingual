def concat(df, *, columns: List[str], new_column: str, sep: str=None):
    """
    Concatenate `columns` element-wise
    See [pandas doc](
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.cat.html) for more information

    ---

    ### Parameters

    *mandatory :*
    - `columns` (*list*): list of columns to concatenate (at least 2 columns)
    - `new_column` (*str*): the destination column

    *optional :*
    - `sep` (*str*): the separator
    """
    if len(columns) < 2:
        raise ValueError('The `columns` parameter needs to have at least 2 columns')
    first_col, *other_cols = columns
    df.loc[:, new_column] = df[first_col].astype(str).str.cat(df[other_cols].astype(str), sep=sep)
    return df