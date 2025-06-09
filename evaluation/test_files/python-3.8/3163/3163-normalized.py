def to_items(self, column_names=None, selection=None, strings=True, virtual=False):
    """Return a list of [(column_name, ndarray), ...)] pairs where the ndarray corresponds to the evaluated data

        :param column_names: list of column names, to export, when None DataFrame.get_column_names(strings=strings, virtual=virtual) is used
        :param selection: {selection}
        :param strings: argument passed to DataFrame.get_column_names when column_names is None
        :param virtual: argument passed to DataFrame.get_column_names when column_names is None
        :return: list of (name, ndarray) pairs
        """
    items = []
    for name in column_names or self.get_column_names(strings=strings, virtual=virtual):
        items.append((name, self.evaluate(name, selection=selection)))
    return items