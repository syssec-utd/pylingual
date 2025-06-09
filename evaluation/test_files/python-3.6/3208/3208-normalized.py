def select_non_missing(self, drop_nan=True, drop_masked=True, column_names=None, mode='replace', name='default'):
    """Create a selection that selects rows having non missing values for all columns in column_names.

        The name reflect Panda's, no rows are really dropped, but a mask is kept to keep track of the selection

        :param drop_nan: drop rows when there is a NaN in any of the columns (will only affect float values)
        :param drop_masked: drop rows when there is a masked value in any of the columns
        :param column_names: The columns to consider, default: all (real, non-virtual) columns
        :param str mode: Possible boolean operator: replace/and/or/xor/subtract
        :param str name: history tree or selection 'slot' to use
        :return:
        """
    column_names = column_names or self.get_column_names(virtual=False)

    def create(current):
        return selections.SelectionDropNa(drop_nan, drop_masked, column_names, current, mode)
    self._selection(create, name)