def get_value(self, column_name_or_i, filter_column_name_or_i, filter_criterion):
    """
        Returns first occurrence of value of filter column matching filter criterion.
        """
    column_i = self._get_column_index(column_name_or_i)
    filter_column_i = self._get_column_index(filter_column_name_or_i)
    filter_fct = {float: lambda x: float(x) == filter_criterion, int: lambda x: int(x) == filter_criterion, str: lambda x: x.lower() == filter_criterion.lower()}[type(filter_criterion)]
    for (row_i, row) in enumerate(self._data):
        if filter_fct(row[filter_column_i]):
            break
    else:
        raise ValueError('Filter did not return any values.')
    return self._data[row_i][column_i]