def fromString(self, string):
    """
        Converts the string to a value using the composed AMP argument, then
        checks all the constraints against that value.
        """
    value = self.baseArgument.fromString(string)
    self._checkConstraints(value)
    return value