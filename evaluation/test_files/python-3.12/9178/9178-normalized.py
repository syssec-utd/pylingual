def rename(df, values: Dict[str, Dict[str, str]]=None, columns: Dict[str, Dict[str, str]]=None, locale: str=None):
    """
    Replaces data values and column names according to the locale

    ---

    ### Parameters

    - `values` (optional: dict):
        - key: term to be replaced
        - value:
            - key: the locale e.g. 'en' or 'fr'
            - value: term's translation
    - `columns` (optional: dict):
        - key: columns name to be replaced
        - value:
            - key: the locale e.g. 'en' or 'fr'
            - value: column name's translation
    - `locale` (optional: str): the locale you want to use.
      By default the client locale is used.

    ---

    ### Example

    **Input**

    | label | value |
    |:----------------:|:-----:|
    | France | 100 |
    | Europe wo France | 500 |

    ```cson
    rename:
      values:
        'Europe wo France':
          'en': 'Europe excl. France'
          'fr': 'Europe excl. France'
      columns:
        'value':
          'en': 'revenue'
          'fr': 'revenue'
    ```

    **Output**

    | label | revenue |
    |:-------------------:|:-------:|
    | France | 100 |
    | Europe excl. France | 500 |

    """
    if values:
        to_replace = list(values.keys())
        value = [values[term][locale] for term in values]
        df = df.replace(to_replace=to_replace, value=value)
    if columns:
        _keys = list(columns.keys())
        _values = [column[locale] for column in columns.values()]
        columns = dict(list(zip(_keys, _values)))
        df = df.rename(columns=columns)
    return df