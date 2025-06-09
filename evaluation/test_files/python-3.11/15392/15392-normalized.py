def parse(self, line):
    """
        Parses a single line from the log file and returns
        a dictionary of it's contents.

        Raises and exception if it couldn't parse the line
        """
    line = line.strip()
    match = self._regex.match(line)
    if match:
        data = {}
        for i, e in enumerate(match.groups()):
            if e == '-':
                k, v = (self._names[i], None)
            else:
                k, v = (self._names[i], self._types[i](e))
            data[k] = v
        return data
    raise ApacheLogParserError('Unable to parse: %s' % line)