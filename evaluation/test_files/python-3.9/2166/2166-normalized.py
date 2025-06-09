def as_list(data, use_pandas=True, header=True):
    """
    Convert an H2O data object into a python-specific object.

    WARNING! This will pull all data local!

    If Pandas is available (and use_pandas is True), then pandas will be used to parse the
    data frame. Otherwise, a list-of-lists populated by character data will be returned (so
    the types of data will all be str).

    :param data: an H2O data object.
    :param use_pandas: If True, try to use pandas for reading in the data.
    :param header: If True, return column names as first element in list

    :returns: List of lists (Rows x Columns).
    """
    assert_is_type(data, H2OFrame)
    assert_is_type(use_pandas, bool)
    assert_is_type(header, bool)
    return H2OFrame.as_data_frame(data, use_pandas=use_pandas, header=header)