def convert_datetime_to_str(df, *, column: str, format: str, new_column: str=None):
    """
    Convert datetime column into string column

    ---

    ### Parameters

    *mandatory :*
    - column (*str*): name of the column to format
    - format (*str*): format of the result values (see [available formats](
    https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior))

    *optional :*
    - new_column (*str*): name of the output column. By default `column` is overwritten.
    """
    new_column = new_column or column
    df[new_column] = df[column].dt.strftime(format)
    return df