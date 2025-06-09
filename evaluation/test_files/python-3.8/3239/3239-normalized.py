def add_column(self, name, data):
    """Add a column to the DataFrame

        :param str name: name of column
        :param data: numpy array with the data
        """
    super(DataFrameArrays, self).add_column(name, data)
    self._length_unfiltered = int(round(self._length_original * self._active_fraction))