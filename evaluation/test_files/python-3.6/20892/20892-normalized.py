def getlist(self, section, option):
    """Read a list of strings.

        The value of `section` and `option` is treated as a comma- and newline-
        separated list of strings.  Each value is stripped of whitespace.

        Returns the list of strings.

        """
    value_list = self.get(section, option)
    values = []
    for value_line in value_list.split('\n'):
        for value in value_line.split(','):
            value = value.strip()
            if value:
                values.append(value)
    return values