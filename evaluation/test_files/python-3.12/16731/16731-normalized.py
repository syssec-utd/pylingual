def items(self):
    """
        Represents the contents of the row as a :code:`dict` with the column
        names as keys, and the row's fields as values.

        :rtype: dict
        """
    return {k.name: v for k, v in zip(self.columns, self)}