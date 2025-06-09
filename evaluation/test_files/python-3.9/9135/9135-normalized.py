def compute_evolution_by_criteria(df, id_cols: List[str], value_col: str, compare_to: str, method: str='abs', format: str='column', offseted_suffix: str='_offseted', evolution_col_name: str='evolution_computed', raise_duplicate_error: bool=True):
    """
    This function answers the question: how has a value changed compare to a specific value ?

    ---

    ### Parameters

    *mandatory :*
    - `id_cols` (*list*): columns used to create each group
    - `value_col` (*str*): name of the column containing the value to compare
    - `compare_to` (*str*): the query identifying a specific set of values for comparison.

    *optional :*
    - `method` (*str*): either `"abs"` for absolute values or `"pct"` for the evolution in percentage of previous value.
    - `offseted_suffix` (*str*): suffix of the offseted column. By default, `"_offseted"`.
    - `evolution_col_name` (*str*): name given to the evolution column. By default, `"evolution_computed"`.
    - `raise_duplicate_error` (*boolean*): raise an error when the dataset has duplicated values with the given `id_cols`.
    - `format` (*str*): `'df'` # Do not change it !!!

    ---

    ### Example

    **Input**

    |   id_cols |    value_col |    month|
    |:---------:|:------------:|:-------:|
    |         A |          100 |        1|
    |           |          250 |       12|
    |         B |          300 |        1|
    |           |          200 |       12|

    ```cson
    compute_evolution_by_criteria:
      id_cols: "id_cols"
      value_col: "value_col"
      compare_to: "month==12"
    ```

    **Output**

    |   id_cols |    value_col |    month|	value_offseted	| evolution_computed|
    |:---------:|:------------:|:-------:|:----------------:|:-----------------:|
    |         A |          100 |        1|               250|               -150|
    |           |          250 |       12|               250|                  0|
    |         B |          300 |        1|               200|                100|
    |           |          200 |       12|               200|                  0|
    """
    return __compute_evolution(**locals())