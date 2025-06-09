def add_aggregation_columns(df, *, group_cols: Union[str, List[str]], aggregations: Dict[str, Agg]):
    """
    Add new columns containing aggregations values on existing columns

    ---

    ### Parameters

    *mandatory :*
    - `group_cols` (*str* or *list*): columns used to aggregate the data
    - `aggregations` (*dict*): keys are name of new columns and values are aggregation functions
       Examples of aggregation functions : 'sum', 'max'
       Available aggregation functions are listed [here](
       https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#aggregation)

    ---

    ### Example

    **Input**

    | ENTITY | YEAR | VALUE_1 | VALUE_2 |
    |:------:|:----:|:-------:|:-------:|
    |    A   | 2017 |    10   |    3    |
    |    A   | 2017 |    20   |    1    |
    |    A   | 2018 |    10   |    5    |
    |    A   | 2018 |    30   |    4    |
    |    B   | 2017 |    60   |    4    |
    |    B   | 2017 |    40   |    3    |
    |    B   | 2018 |    50   |    7    |
    |    B   | 2018 |    60   |    6    |

    ```cson
    add_aggregation_columns:
      group_cols: ['ENTITY', 'YEAR']
      aggregations:
        sum_value1:
          VALUE_1: 'sum'  # sum of `VALUE_1` put in `sum_value1` column
        max_value1:
          VALUE_1: 'max'  # max of `VALUE_1` put in `max_value1` column
        mean_value2:
          VALUE_2: 'mean'  # mean of `VALUE_2` put in `mean_value2` column
    ]
    ```

    **Output**

    | ENTITY | YEAR | VALUE_1 | VALUE_2 | sum_value1 | max_value1 | mean_value2 |
    |:------:|:----:|:-------:|:-------:|:----------:|:----------:|:-----------:|
    |    A   | 2017 |    10   |    3    |     30     |     20     |     2.0     |
    |    A   | 2017 |    20   |    1    |     30     |     20     |     2.0     |
    |    A   | 2018 |    10   |    5    |     40     |     30     |     4.5     |
    |    A   | 2018 |    30   |    4    |     40     |     30     |     4.5     |
    |    B   | 2017 |    60   |    4    |    100     |     60     |     3.5     |
    |    B   | 2017 |    40   |    3    |    100     |     60     |     3.5     |
    |    B   | 2018 |    50   |    7    |    110     |     60     |     6.5     |
    |    B   | 2018 |    60   |    6    |    110     |     60     |     6.5     |

    """
    group = df.groupby(group_cols)
    for new_col, aggs in aggregations.items():
        assert len(aggs) == 1
        (col, agg), *_ = aggs.items()
        df[new_col] = group[col].transform(agg)
    return df