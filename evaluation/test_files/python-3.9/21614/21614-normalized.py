def _format_as_columns(self, items, separator='  '):
    """ Transform a list of strings into a single string with columns.

        Parameters
        ----------
        items : sequence of strings
            The strings to process.

        separator : str, optional [default is two spaces]
            The string that separates columns.

        Returns
        -------
        The formatted string.
        """
    width = self._control.viewport().width()
    char_width = QtGui.QFontMetrics(self.font).width(' ')
    displaywidth = max(10, width / char_width - 1)
    return columnize(items, separator, displaywidth)