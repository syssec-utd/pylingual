def _unsorted_set(df, label, **kwargs):
    """
    Returns a set as inp string with unsorted option.
    """
    out = '*NSET, NSET={0}, UNSORTED\n'.format(label)
    labels = df.index.values
    return out + argiope.utils.list_to_string(labels, **kwargs)