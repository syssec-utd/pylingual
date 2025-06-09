def _compute_value_diff(df, start, end, groups):
    """
    Compute diff value between start and end
    Args:
        df(dataframe):

    Returns: Dataframe

    """
    start_values = df[df['date'] == start['id']].copy()
    end_values = df[df['date'] == end['id']].copy()
    merge_on = []
    for key, group in groups.items():
        merge_on = merge_on + [key, f'{key}_label', f'{key}_order']
    df = start_values.merge(end_values, on=merge_on, how='outer', suffixes=('_start', '_end'))
    df[['value_start', 'value_end']] = df[['value_start', 'value_end']].fillna(0)
    df['value'] = df['value_end'] - df['value_start']
    df.drop(['date_start', 'date_end', 'value_end'], axis=1, inplace=True)
    df.rename(columns={'upperGroup': 'groups'}, inplace=True)
    return df