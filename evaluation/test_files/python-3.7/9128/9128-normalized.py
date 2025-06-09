def top(df, value: str, limit: int, order: str='asc', group: Union[str, List[str]]=None):
    """
    Get the top or flop N results based on a column value for each specified group columns

    ---

    ### Parameters

    *mandatory :*
    - `value` (*str*): column name on which you will rank the results
    - `limit` (*int*): Number to specify the N results you want to retrieve.
        Use a positive number x to retrieve the first x results.
        Use a negative number -x to retrieve the last x results.

    *optional :*
    - `order` (*str*): `"asc"` or `"desc"` to sort by ascending ou descending order. By default : `"asc"`.
    - `group` (*str*, *list of str*): name(s) of columns on which you want to perform the group operation.

    ---

    ### Example

    **Input**

    | variable | Category | value |
    |:--------:|:--------:|:-----:|
    |   lili   |    1     |  50  |
    |   lili   |    1     |  20  |
    |   toto   |    1     |  100  |
    |   toto   |    1     |  200  |
    |   toto   |    1     |  300  |
    |   lala   |    1     |  100  |
    |   lala   |    1     |  150  |
    |   lala   |    1     |  250  |
    |   lala   |    2     |  350  |
    |   lala   |    2     |  450  |


    ```cson
    top:
      value: 'value'
      limit: 4
      order: 'asc'
    ```

    **Output**

    | variable | Category | value |
    |:--------:|:--------:|:-----:|
    |   lala   |    1     |  250  |
    |   toto   |    1     |  300  |
    |   lala   |    2     |  350  |
    |   lala   |    2     |  450  |
    """
    ascending = order != 'desc'
    limit = int(limit)
    filter_func = 'nlargest' if (limit > 0) ^ ascending else 'nsmallest'

    def _top(df):
        return getattr(df, filter_func)(abs(limit), value).sort_values(by=value, ascending=ascending)
    if group is None:
        df = _top(df)
    else:
        df = df.groupby(group).apply(_top)
    return df